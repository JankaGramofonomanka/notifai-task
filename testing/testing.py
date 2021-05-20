import os
import unittest
from argparse import ArgumentParser
import time

import requests
from typing import Dict, Any, Tuple, Union

# status codes
OK = 200
CREATED = 201
NOT_FOUND = 404
UNAUTHORIZED = 401
BAD_REQUEST = 400





class TestApp(unittest.TestCase):

    def setUp(self):

        self.host = os.environ["HOST"]
        self.password = os.environ["PASSWORD"]
        self.token = self.get_token()
        self.token_exp_time = 0.08

        self.post_content = "whatever"
        self.data = {"content": self.post_content}


    # -- UTILITIES ------------------------------------------------------------
    def get_token(self) -> str:
        """
        Returns an access token to the app
        """
        
        data = {"password": self.password}
        received, status_code = self.post("login", data=data, authorized=False)
        self.assertEqual(status_code, OK)

        self.assertDictSchema(received, token=str)
        return received["token"]
    

    def send_request(
        self, 
        method      : str,
        endpoint    : str, 
        data        : Union[None, Dict[str, str]]   = None,
        authorized  : bool                          = True,
        wrong_token : Union[None, str]              = None,
    ) -> Tuple[Dict[str, Any], int]:
        """
        Sends a request to the app

        Parameters
        ----------
        method      : str
        endpoint    : str
        data        : dict or none
        
        authorized  : bool
            True    -> the request contains the acces token `self.token`
            False   -> the request contains no acces token
        
        wrong_token : str or None
            None    -> default token or no token is sent (see `authorized`)
            _       -> the access token is overwriten by `wrong_token`.
                        (if `authorized` == False, no token is sent)
        """

        if method == "GET":
            func = requests.get

        elif method == "POST":
            func = requests.post

        elif method == "PUT":
            func = requests.put

        elif method == "DELETE":
            func = requests.delete

        else:
            raise ValueError(f"Unknown method: {method}")

        if len(endpoint) > 0 and endpoint[0] == "/":
            endpoint = endpoint[1:]

        headers = {}
        if authorized:

            if wrong_token:
                headers["x-access-tokens"] = wrong_token

            else:    
                headers["x-access-tokens"] = self.token

        response = func(f"{self.host}/{endpoint}", json=data, headers=headers)

        return response.json(), response.status_code


    def get(self, *args, **kwargs) -> Tuple[Dict[str, Any], int]:
        return self.send_request("GET", *args, **kwargs)
    
    def post(self, *args, **kwargs) -> Tuple[Dict[str, Any], int]:
        return self.send_request("POST", *args, **kwargs)
    
    def put(self, *args, **kwargs) -> Tuple[Dict[str, Any], int]:
        return self.send_request("PUT", *args, **kwargs)
    
    def delete(self, *args, **kwargs) -> Tuple[Dict[str, Any], int]:
        return self.send_request("DELETE", *args, **kwargs)


    # -- CUSTOM ASSERT METHODS ------------------------------------------------
    def assertDictSchema(self, data : Dict[str, Any], **kwargs : type):
        """
        Asserts that `data` is a dict, and has the correct schema
        """

        self.assertIsInstance(data, dict)
        for key, expected_type in kwargs.items():

            self.assertIn(key, data.keys())
            self.assertIsInstance(data[key], expected_type)


    def assertDictContent(self, data : Dict[str, Any], **kwargs : Any):
        """
        Asserts that `data` is a dict, and has the correct keys and values
        """

        self.assertIsInstance(data, dict)
        for key, expected_value in kwargs.items():

            self.assertIn(key, data.keys())
            self.assertEqual(data[key], expected_value)



    # -- ACTUAL TESTS ---------------------------------------------------------
    def test_expected(self):
        """
        Tests the expected case, (requests are authorized, content valid etc.)
        """
        
        # create a post
        received, status_code = self.post("create", data=self.data)
        self.assertEqual(status_code, CREATED)
        self.assertDictSchema(received, id=str)

        post_id = received["id"]

        # view the post
        for i in range(3):
            received, status_code = self.get(post_id, authorized=False)
            self.assertEqual(status_code, OK)
            self.assertDictContent(
                received, 
                content=self.post_content, views=i
            )
        
        # edit the post
        new_post_content = "revetahw"
        new_data = {"content": new_post_content}
        received, status_code = self.put(post_id, data=new_data)
        self.assertEqual(status_code, OK)
        self.assertDictSchema(received, message=str)

        # view the post again
        received, status_code = self.get(post_id)
        self.assertEqual(status_code, OK)
        self.assertDictContent(received, content=new_post_content, views=0)

        # delete the post
        received, status_code = self.delete(post_id)
        self.assertEqual(status_code, OK)
        self.assertDictSchema(received, message=str)



    def test_not_found(self):
        """
        Test case when requests want access to non existent posts
        """
        
        # create a post to get its id and then delete it
        received, status_code = self.post("create", data=self.data)
        self.assertEqual(status_code, CREATED)
        self.assertDictSchema(received, id=str)

        post_id = received["id"]

        # delete the post
        received, status_code = self.delete(post_id)
        self.assertEqual(status_code, OK)
        self.assertDictSchema(received, message=str)

        # try to view the post
        received, status_code = self.get(post_id)
        self.assertEqual(status_code, NOT_FOUND)
        self.assertDictSchema(received, message=str)

        # try to edit the post
        received, status_code = self.put(post_id, data=self.data)
        self.assertEqual(status_code, NOT_FOUND)
        self.assertDictSchema(received, message=str)

        # try to delete the post
        received, status_code = self.delete(post_id)
        self.assertEqual(status_code, NOT_FOUND)
        self.assertDictSchema(received, message=str)
        


    def test_authorization(self):
        """
        Tests if unauthorized requests are rejected
        """

        # try to create a post
        token = "t0T4l1y.VaL1D.T0k3n"
        types_of_unauthorization = {"authorized": False, "wrong_token": token}

        for key, value in types_of_unauthorization.items():

            received, status_code = self.post(
                "create", data=self.data, **{key: value})
            self.assertEqual(status_code, UNAUTHORIZED)
            self.assertDictSchema(received, message=str)
        

        # post a post so that to have an id of an existing post
        received, status_code = self.post("create", data=self.data)
        self.assertEqual(status_code, CREATED)
        self.assertDictSchema(received, id=str)
        post_id = received["id"]

        # try to edit the post
        for key, value in types_of_unauthorization.items():

            received, status_code = self.put(
                post_id, data=self.data, **{key: value})
            self.assertEqual(status_code, UNAUTHORIZED)
            self.assertDictSchema(received, message=str)
        
        # try to delete the post
        for key, value in types_of_unauthorization.items():

            received, status_code = self.delete(post_id, **{key: value})
            self.assertEqual(status_code, UNAUTHORIZED)
            self.assertDictSchema(received, message=str)
        
        # delete the post to not grow the database while testing
        received, status_code = self.delete(post_id)
        self.assertEqual(status_code, OK)
        self.assertDictSchema(received, message=str)
    
    
    def test_expiration(self):

        # wait for the token to expire
        time.sleep(self.token_exp_time * 60 + 5)

        # try to create a post
        received, status_code = self.post("create", data=self.data)
        self.assertEqual(status_code, UNAUTHORIZED)
        self.assertDictSchema(received, message=str)
    

        



if __name__ == "__main__":
    unittest.main()

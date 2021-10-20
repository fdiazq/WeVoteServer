# apis_v1/test_campaign_retrieve.py
# Brought to you by We Vote. Be good.
# -*- coding: UTF-8 -*-

from django.urls import reverse
from django.test import TransactionTestCase
from django.test import Client
from voter.models import VoterDeviceLink
 
import json

# Inheriting from TransactionTestCase enables test mirror to redirect queries from 'readonly' database to 'default'.

class WeVoteAPIsV1TestsCampaignRetrieve(TransactionTestCase):
    databases = ["default", "readonly"]


    def setUp(self):
 
        self.voter_create_url = reverse("apis_v1:voterCreateView")
        self.voter_retrieve_url = reverse("apis_v1:voterRetrieveView")
        self.generate_voter_device_id_url = reverse("apis_v1:deviceIdGenerateView")
        self.campaign_save_url = reverse("apis_v1:campaignSaveView")
        self.campaign_retrieve_url = reverse("apis_v1:campaignRetrieveView")
        self.campaign_retrieve_as_owner_url = reverse("apis_v1:campaignRetrieveAsOwnerView")
        # Creating Client object enables passing in META data to the request object.
        self.client2 = Client(HTTP_USER_AGENT='Mozilla/5.0')
        
 
    def test_campaign_retrieve_with_no_voter_device_id(self):
        voter = self.client
        
        campaign = self.client.get(self.campaign_save_url)
        json001 = json.loads(campaign.content.decode())
        print("\ncampaign_save_url:" + "\n")
        print(json001)
        
        campaign02 = self.client.get(self.campaign_retrieve_url)
        json002 = json.loads(campaign02.content.decode())
        print("\ncampaign_retrieve_url:" + "\n")
        print(json002)
        
    
    def test_campaign_retrieve_with_no_voter_device_id(self):
        voter = self.client
        
        campaign = self.client.get(self.campaign_save_url)
        json001 = json.loads(campaign.content.decode())
        print("\ncampaign_save_url:" + "\n")
        print(json001)
        
        campaign02 = self.client.get(self.campaign_retrieve_url)
        json002 = json.loads(campaign02.content.decode())
        print("\ncampaign_retrieve_url:" + "\n")
        print(json002)
        
        response1 = self.client.get(self.campaign_retrieve_as_owner)
        json_data = json.loads(response1.content.decode())
        print("\ncampaign_retrieve_as_owner:" + "\n")
        print(json_data)
        
        response1 = self.client2.get(self.campaign_retrieve_url)
        json_data1 = json.loads(response1.content.decode())
        # print("\ncampaign_retrieve_url:" + "\n")
        # print(json002)
        # print(response1.content)

        self.assertEqual('status' in json_data1,
                         True,
                         "status expected in the json response, and not found")

        self.assertEqual(json_data1['status'],
                         "CAMPAIGNX_NOT_FOUND-MISSING_VARIABLES CAMPAIGNX_RETRIEVE_ERROR ",
                         "status = {status} Expected status CAMPAIGNX_NOT_FOUND-MISSING_VARIABLES CAMPAIGNX_RETRIEVE_ERROR ".format(status=json_data1['status']))

        self.assertEqual(json_data1['success'],
                         False,
                         "success = {success} Expected fail".format(success=json_data1['success']))
        
        response2 = self.client2.get(self.campaign_retrieve_as_owner_url)
        json_data2 = json.loads(response2.content.decode())
        # print("\ncampaign_retrieve_as_owner:" + "\n")
        # print(json_data)
        # print(response2.content)

        self.assertEqual('status' in json_data2,
                         True,
                         "status expected in the json response, and not found")

        self.assertEqual(json_data2['status'],
                         "VALID_VOTER_ID_MISSING ",
                         "status = {status} Expected status VALID_VOTER_ID_MISSING ".format(status=json_data2['status']))

        self.assertEqual(json_data2['success'],
                         False,
                         "success = {success} Expected fail".format(success=json_data2['success']))


    def test_campaign_retrieve_with_voter_device_id_but_no_voter_id(self):

        response1 = self.client2.get(self.generate_voter_device_id_url)
        json_data1 = json.loads(response1.content.decode())

        print("\ngenerate_voter_device_id_url:" + "\n")
        print(response1.content)
        # campaignx = CampaignX.objects.using('readonly').get(we_vote_id=campaignx_we_vote_id)
        # print("Campaign: ")
        # print(campaignx)
        # voter = Voter.objects.using('readonly').get(we_vote_id=campaignx_we_vote_id)

        self.assertEqual('voter_device_id' in json_data1,
                         True,
                         "voter_device_id expected in the json response, and not found")

        self.assertEqual(json_data1['status'],
                         "DEVICE_ID_GENERATE_VALUE_DOES_NOT_EXIST",
                         "status = {status} Expected status DEVICE_ID_GENERATE_VALUE_DOES_NOT_EXIST".format(status=json_data1['status']))

        self.assertEqual(json_data1['success'],
                         True,
                         "success = {success} Expected success".format(success=json_data1['success']))                         

        voter_device_id = json_data1['voter_device_id'] if 'voter_device_id' in json_data1 else ''

        # device_entry = VoterDeviceLink.objects.using('readonly').all().values()
        # print("Device ID: ")
        # print(device_entry)

        response2 = self.client2.get(self.voter_create_url, {'voter_device_id': voter_device_id})
        json_data2 = json.loads(response2.content.decode())

        self.assertEqual('voter_we_vote_id' in json_data2,
                         True,
                         "voter_we_vote_id expected in the json response, and not found")

        self.assertEqual(json_data2['status'],
                         "VOTER_CREATED",
                         "status = {status} Expected status VOTER_CREATED".format(status=json_data2['status']))

        self.assertEqual(json_data2['success'],
                         True,
                         "success = {success} Expected success".format(success=json_data2['success']))

        voter_we_vote_id = json_data2['voter_we_vote_id'] if 'voter_we_vote_id' in json_data2 else ''

        print("\nvoter_create_url:" + "\n")
        print(response2.content)
        print("\nVoter WVID: " + voter_we_vote_id)

        response3 = self.client2.get(self.voter_retrieve_url, {'voter_device_id': voter_device_id})
        json_data3 = json.loads(response3.content.decode())

        self.assertEqual('linked_organization_we_vote_id' in json_data3,
                         True,
                         "linked_organization_we_vote_id expected in the json response, and not found")

        self.assertEqual(json_data3['status'],
                         "VOTER_RETRIEVE_START VOTER_DEVICE_ID_RECEIVED VOTER_FOUND VOTER.LINKED_ORGANIZATION_WE_VOTE_ID-MISSING EXISTING_ORGANIZATION_NOT_FOUND ORGANIZATION_CREATED FACEBOOK_LINK_TO_VOTER_NOT_FOUND ",
                         "status = {status} Expected status VOTER_RETRIEVE_START VOTER_DEVICE_ID_RECEIVED VOTER_FOUND VOTER.LINKED_ORGANIZATION_WE_VOTE_ID-MISSING EXISTING_ORGANIZATION_NOT_FOUND ORGANIZATION_CREATED FACEBOOK_LINK_TO_VOTER_NOT_FOUND ".format(status=json_data3['status']))

        self.assertEqual(json_data3['success'],
                         True,
                         "success = {success} Expected success".format(success=json_data3['success']))

        organization_we_vote_id = json_data3["linked_organization_we_vote_id"] if "linked_organization_we_vote_id" in json_data3 else ''

        print("\nvoter_retrieve_url:" + "\n")
        print(response3.content) 

        response4 = self.client2.get(self.campaign_save_url, {'voter_device_id': voter_device_id, 'voter_we_vote_id': voter_we_vote_id, 'organization_we_vote_id': organization_we_vote_id, 'in_draft_mode': False, 'in_draft_mode_changed': True})
        json_data4 = json.loads(response4.content.decode())

        self.assertEqual('campaignx_we_vote_id' in json_data4,
                         True,
                         "campaignx_we_vote_id expected in the json response, and not found")

        self.assertEqual(json_data4['status'],
                         "CAMPAIGNX_OWNER_CREATED RETRIEVE_CAMPAIGNX_AS_OWNER-VOTER_WE_VOTE_ID-NOT_FOUND CAMPAIGNX_CREATED ",
                         "status = {status} Expected status CAMPAIGNX_OWNER_CREATED RETRIEVE_CAMPAIGNX_AS_OWNER-VOTER_WE_VOTE_ID-NOT_FOUND CAMPAIGNX_CREATED ".format(status=json_data4['status']))

        self.assertEqual(json_data4['success'],
                         True,
                         "success = {success} Expected success".format(success=json_data4['success']))

        campaignx_we_vote_id = json_data4["campaignx_we_vote_id"] if "campaignx_we_vote_id" in json_data4 else ''
        print("\ncampaign_save_url:" + "\n")
        # print(json_data4)
        print(response4.content)
        # Need an organization_we_vote_id???

        response5 = self.client2.get(self.campaign_retrieve_url, {'voter_device_id': voter_device_id, 'campaignx_we_vote_id': campaignx_we_vote_id})
        json_data5 = json.loads(response5.content.decode())

        self.assertEqual('campaignx_we_vote_id' in json_data5,
                         True,
                         "campaignx_we_vote_id expected in the json response, and not found")

        self.assertEqual(json_data5['status'],
                         "CAMPAIGNX_FOUND_WITH_WE_VOTE_ID ",
                         "status = {status} Expected status CAMPAIGNX_FOUND_WITH_WE_VOTE_ID ".format(status=json_data5['status']))

        self.assertEqual(json_data5['success'],
                         True,
                         "success = {success} Expected success".format(success=json_data5['success']))

        print("\ncampaign_retrieve_url:" + "\n")
        # print(json_data5)
        print(response5.content)

        response6 = self.client2.get(self.campaign_retrieve_as_owner_url, {'voter_device_id': voter_device_id, 'campaignx_we_vote_id': campaignx_we_vote_id})
        json_data6 = json.loads(response6.content.decode())

        self.assertEqual('campaignx_we_vote_id' in json_data6,
                         True,
                         "campaignx_we_vote_id expected in the json response, and not found")

        self.assertEqual(json_data6['status'],
                         "RETRIEVE_CAMPAIGNX_AS_OWNER_FOUND_WITH_WE_VOTE_ID ",
                         "status = {status} Expected status RETRIEVE_CAMPAIGNX_AS_OWNER_FOUND_WITH_WE_VOTE_ID ".format(status=json_data6['status']))

        self.assertEqual(json_data6['success'],
                         True,
                         "success = {success} Expected success".format(success=json_data6['success']))        

        print("\ncampaign_retrieve_as_owner:" + "\n")
        # print(json_data6)
        print(response6.content)

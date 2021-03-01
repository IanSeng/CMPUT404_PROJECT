from django.test import TestCase
from nodes.models import Node
from django.contrib.auth import get_user_model
import re

class NodeTestCase(TestCase):
    def setUp(self):
        self.hostname = 'www.example.com'
        self.remote_url = f'https://{self.hostname}'
        self.remote_username = 'username'
        self.remote_password = 'password'
        self.admin_approval = True

        self.our_username = 'konnection_username'
        self.our_password = 'konnection_password'

        self.node = self.create_node(self.admin_approval)

    def tearDown(self):
        pass

    def create_node(self, admin_approval):
        node = Node.objects.create(
            remote_server_url=self.remote_url,
            remote_server_username=self.remote_username,
            remote_server_password=self.remote_password,
            adminApproval=admin_approval,
            konnection_username=self.our_username,
            konnection_password=self.our_password
        )
        return node
    
    def test_create_node(self):
        """Test creation of Node Object"""
        self.assertTrue(isinstance(self.node, Node))

        self.assertEqual(self.node.remote_server_url, self.remote_url)
        self.assertEqual(self.node.remote_server_username, self.remote_username)
        self.assertEqual(self.node.remote_server_password, self.remote_password)
        self.assertEqual(self.node.adminApproval, self.admin_approval)
        self.assertEqual(self.node.konnection_username, self.our_username)
        self.assertEqual(self.node.konnection_password, self.our_password)
    
    def test_create_node_also_creates_author(self):
        """Test creation of Author Object"""
        self.assertEqual(get_user_model().objects.filter(username=self.remote_username).exists(), True)

    def test_unset_admin_approval_if_missing_server_url(self):
        """Test unset Author adminApproval if remote_server_url is missing"""
        self.assertEqual(
            get_user_model().objects.get(username=self.remote_username).adminApproval,
            True
        )

        self.node.remote_server_url = None
        self.node.save()
        
        self.assertEqual(
            get_user_model().objects.get(username=self.remote_username).adminApproval,
            False
        )

    def test_unset_admin_approval_if_missing_server_password(self):
        """Test unset Author adminApproval if remote_server_password is missing"""
        self.assertEqual(
            get_user_model().objects.get(username=self.remote_username).adminApproval,
            True
        )

        self.node.remote_server_password = ''
        self.node.save()
        
        self.assertEqual(
            get_user_model().objects.get(username=self.remote_username).adminApproval,
            False
        )

    
    def test_change_to_admin_approval_will_refect_in_author(self):
        """Test change to admin approval will reflect in author"""
        self.assertEqual(
            get_user_model().objects.get(username=self.remote_username).adminApproval,
            True
        )

        self.node.adminApproval = False
        self.node.save()

        self.assertEqual(
            get_user_model().objects.get(username=self.remote_username).adminApproval,
            False
        )

        self.node.adminApproval = True
        self.node.save()

        self.assertEqual(
            get_user_model().objects.get(username=self.remote_username).adminApproval,
            True
        )     
    
    def test_hostname(self):
        self.assertEqual(self.node.hostname(),self.hostname)

    def test_empty_username_field_changes_to_hostname(self):
        """Test empty username field will have hostname as its value"""
        
        self.node.remote_server_username = ''
        self.node.save()

        self.assertEqual(
            self.node.remote_server_username,
            re.sub(r'\W+', '', self.hostname)
        )
    
    def test_delete_author_if_node_is_deleted(self):
        self.assertEqual(get_user_model().objects.filter(username=self.remote_username).exists(), True)
        self.node.delete()
        self.assertEqual(len(Node.objects.all()), 0)
        self.assertEqual(get_user_model().objects.filter(username=self.remote_username).exists(), False)
    
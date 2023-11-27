"""
TodoApp - Interacting with a Todo List Smart Contract on Binance Smart Chain

This script provides a Python class, TodoApp, for interacting with a smart contract representing a Todo List on the Binance Smart Chain using MetaMask.

Requirements:
- Python 3.x
- web3 library (install using: pip install web3)

Note: Ensure that the required dependencies are installed before running the script.

Usage:
1. Create an instance of TodoApp by providing the contract address, ABI (Application Binary Interface), wallet address, wallet private key, and a web3 instance.
2. Use the provided methods to interact with the Todo List smart contract.

"""

from web3 import Web3
import json
import time
import web3.exceptions as exceptions

# CONSTANTS
METAMASK_RPC_URL = "https://data-seed-prebsc-1-s1.binance.org:8545"
CONTRACT_ADDRESS = "0xe82D1C7E9640d71679DA8f60A0d891279fE8f051"
WALLET_ADDRESS = "0xBdae311f9F0AF55A28cABB1f397Db365c574ed3b"
WALLET_PRIVATE_KEY = ""

# Code abi from remix compilation
with open('abi.json') as f:
    abi = json.load(f)


# Connect to MetaMask
w3 = Web3(Web3.HTTPProvider(METAMASK_RPC_URL))

# Contract instance creation
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)


class TodoApp:
    def __init__(self, contract_address, contract_abi, wallet_address, wallet_private_key, w3):
        self.contract = w3.eth.contract(address=contract_address, abi=contract_abi)
        self.wallet_address = wallet_address
        self.wallet_private_key = wallet_private_key
        self.w3 = w3

    def addTask(self, task_description):
        """
        Adds a new task to the Todo List.

        Args:
            task_description (str): The description of the task.

        Returns:
            None
        """

        transaction = self.contract.functions.addTask(task_description).build_transaction(
            {"gasPrice": self.w3.eth.gas_price,
             "chainId": self.w3.eth.chain_id,
             "from": self.wallet_address,
             "nonce": self.w3.eth.get_transaction_count(self.wallet_address)})

        signed_transaction = self.w3.eth.account.sign_transaction(transaction, self.wallet_private_key)
        self.w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

    def markTaskCompleted(self, task_id_):
        """
        Marks a task as completed in the Todo List.

        Args:
            task_id_ (int): The ID of the task to mark as completed.

        Returns:
            None
        """

        try:
            transaction = self.contract.functions.markTaskCompleted(task_id_).build_transaction(
                {"gasPrice": self.w3.eth.gas_price,
                 "chainId": self.w3.eth.chain_id,
                 "from": self.wallet_address,
                 "nonce": self.w3.eth.get_transaction_count(self.wallet_address)})
            
            signed_transaction = self.w3.eth.account.sign_transaction(transaction, self.wallet_private_key)
            self.w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
            print(f"Task {task_id_} marked as completed")
        except exceptions.ContractLogicError:
            print(f"Task {task_id_} already completed")

    def getAllTasks(self):
        """
        Retrieves all tasks from the Todo List.

        Returns:
            tuple: A tuple containing lists of task IDs, task descriptions, and completion statuses.
        """

        return self.contract.functions.getAllTasks().call()

    def printAllTasks(self):
        """
        Prints information about all tasks in the Todo List.

        Returns:
            None
        """

        tasks = self.getAllTasks()
        for task_number in range(len(tasks[1])):
            task_id = tasks[0][task_number]
            task_content = tasks[1][task_number]
            task_completed = tasks[2][task_number]

            print("*******************************")
            print(f"Task number :{task_number + 1}")
            print(f"Task ID: {task_id}")
            print(f"Task Content: {task_content}")
            print(f"Task Completed: {task_completed}")

    def getTaskByContent(self, task_content):
        """
        Retrieves information about a task by its content.

        Args:
            task_content (str): The description of the task.

        Returns:
            tuple: A tuple containing the task ID, task content, and completion status.
        """

        try:
            return self.contract.functions.getTaskByContent(task_content).call()
        except exceptions.ContractLogicError:
            print("Task not found")

    def getTask(self, task_id):
        """
        Retrieves information about a task by its ID.

        Args:
            task_id (int): The ID of the task.

        Returns:
            tuple: A tuple containing the task content and completion status.
        """

        return self.contract.functions.getTask(task_id).call()

    def deleteTask(self, task_id_):
        """
        Deletes a task from the Todo List.

        Args:
            task_id_ (int): The ID of the task to delete.

        Returns:
            None
        """
        transaction = self.contract.functions.deleteTask(task_id_).build_transaction(
            {"gasPrice": self.w3.eth.gas_price,
             "chainId": self.w3.eth.chain_id,
             "from": self.wallet_address,
             "nonce": self.w3.eth.get_transaction_count(self.wallet_address)})

        signed_transaction = self.w3.eth.account.sign_transaction(transaction, self.wallet_private_key)
        self.w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

        print(f"Task {task_id_} deleted")

    def updateTask(self, task_id_, _newContent, _newCompleted):
        """
        Updates the content and completion status of a task in the Todo List.

        Args:
            task_id_ (int): The ID of the task to update.
            _newContent (str): The new content for the task.
            _newCompleted (bool): The new completion status for the task.

        Returns:
            None
        """

        transaction = self.contract.functions.updateTask(task_id_, _newContent, _newCompleted).build_transaction(
            {"gasPrice": self.w3.eth.gas_price,
             "chainId": self.w3.eth.chain_id,
             "from": self.wallet_address,
             "nonce": self.w3.eth.get_transaction_count(self.wallet_address)})

        signed_transaction = self.w3.eth.account.sign_transaction(transaction, self.wallet_private_key)
        self.w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

    def delete_all_tasks(self):
        """
        Deletes all tasks in the Todo List.

        This method retrieves all tasks and deletes each one in sequence with a delay of 5 seconds between deletions.

        Args:
            None

        Returns:
            None
        """

        tasks = self.getAllTasks()
        for i in range(len(tasks[0])):
            App.deleteTask(1)
            time.sleep(5)


App = TodoApp(CONTRACT_ADDRESS, abi, WALLET_ADDRESS, WALLET_PRIVATE_KEY, w3)

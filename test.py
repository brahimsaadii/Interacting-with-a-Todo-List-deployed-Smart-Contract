import unittest
import time
from web3 import Web3, HTTPProvider
from TodoAPP import TodoApp, METAMASK_RPC_URL, CONTRACT_ADDRESS, abi, WALLET_ADDRESS, WALLET_PRIVATE_KEY

w3 = Web3(Web3.HTTPProvider(METAMASK_RPC_URL))

# from contract import contract
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)



class TestAddTask(unittest.TestCase):

    def setUp(self):
        self.contract = TodoApp(CONTRACT_ADDRESS, abi, WALLET_ADDRESS, WALLET_PRIVATE_KEY, w3)
    
    def test_add_task_success(self):
        task_description = 'Learn Solidity'

        # Send transaction to add the task
        self.contract.addTask(task_description)
        time.sleep(5)
        # Check if the task is added
        tasks = self.contract.getAllTasks()
        
        added_index = tasks[0][-1] - 1

        task_content = tasks[1][added_index]
        task_completed = tasks[2][added_index]

        if task_content == task_description and task_completed == False:
            self.assertTrue(True)
        else:
            self.fail('Task not added')


    def test_mark_task_completed(self):
        # Add a task and mark it as completed
        task_description = "Complete this task"

        self.contract.addTask(task_description)
        time.sleep(5)
        self.contract.markTaskCompleted(self.contract.getAllTasks()[0][-1])
        time.sleep(5)
        # Check if task is completed
        self.assertTrue(self.contract.getAllTasks()[2][-1])

    def test_get_all_tasks(self):
        # Add a few tasks
        old_tasks = self.contract.getAllTasks()
        time.sleep(10)
        self.contract.addTask("testing task")
        time.sleep(10)
        # Retrieve all tasks
        all_tasks = self.contract.getAllTasks()

        # Check if all tasks were retrieved
        self.assertTrue(len(all_tasks[1]) == 1 + len(old_tasks[1]))

    def test_get_task_by_content(self):
        # Add a task and get it by content
        task_description = "Unique task content"
        self.contract.addTask(task_description)
        time.sleep(10)
        task_info = self.contract.getTaskByContent(task_description)

        # Check if the retrieved task matches the added one
        self.assertTrue(task_info[1] == task_description)

    def test_get_task(self):
        # Add a task and get it by ID
        task_description = "Another task"
        self.contract.addTask(task_description)
        time.sleep(10)
        tasks = self.contract.getAllTasks()
        task_info = self.contract.getTask(tasks[0][-1])

        # Check if the retrieved task matches the added one
        self.assertEqual(task_info[1], task_description)

    def test_delete_task(self):
        # Add a task and delete it
        task_description = "Task to be deleted"
        self.contract.addTask(task_description)
        time.sleep(10)
        tasks = self.contract.getAllTasks()
        self.contract.deleteTask(tasks[0][-1])
        time.sleep(10)

        # Check if the task was deleted
        tasks = self.contract.getAllTasks()
        self.assertNotIn(task_description, tasks[1])

    def test_update_task(self):
        # Add a task and update it
        task_description = "Task to be updated"
        self.contract.addTask(task_description)
        time.sleep(10)
        id_task_to_be_apdated = self.contract.getAllTasks()[0][-1]
        # Update task content and completion status
        self.contract.updateTask(id_task_to_be_apdated, "Updated task content", True)
        time.sleep(10)
        tasks = self.contract.getAllTasks()
        # Retrieve updated task
        task_info = self.contract.getTask(tasks[0][-1])

        # Check if the task was updated
        self.assertEqual(task_info[1], "Updated task content")
        self.assertTrue(task_info[2])


if __name__ == "__main__":
    unittest.main()

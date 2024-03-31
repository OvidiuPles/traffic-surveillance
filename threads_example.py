import concurrent.futures
import time
num_functions = 7


def your_function(index):
    print(f"Function {index} started")
    time.sleep(0.1)  # Simulating some work with a sleep of 1 second
    print(f"Function {index} finished")


start = time.perf_counter()
with concurrent.futures.ThreadPoolExecutor(max_workers=num_functions) as executor:
    futures = [executor.submit(your_function, i) for i in range(num_functions)]
    concurrent.futures.wait(futures)
stop = time.perf_counter()
print(f"time: {stop - start}")

for i in range(7):
    print(i)






#  cassic threads
# import threading
# import time
#
#
# # Function to print numbers from 1 to 5 with a delay
# def print_numbers():
#     for i in range(1, 6):
#         print(i)
#         time.sleep(1)
#
#
# # Function to print letters from 'a' to 'e' with a delay
# def print_letters():
#     for char in 'abcde':
#         print(char)
#         time.sleep(1)
#
#
# # Creating threads for each function
# thread1 = threading.Thread(target=print_numbers)
# thread2 = threading.Thread(target=print_letters)
#
# # Starting both threads
# thread1.start()
# thread2.start()
#
# # Waiting for both threads to finish
# thread1.join()
# thread2.join()
#
# print("Both threads have finished execution.")

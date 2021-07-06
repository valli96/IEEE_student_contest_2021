import multiprocessing
import time

def analysis_timeout_handler(procnum, return_dict):
    """worker function"""
    print(str(procnum) + " represent!")
    time.sleep(1)
    return_dict[procnum] = "Hallo ich bin raus"


if __name__ == "__main__":
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    jobs = []
    p = multiprocessing.Process(target=analysis_timeout_handler, args=(1, return_dict))
    jobs.append(p)
    # import ipdb; ipdb.set_trace()
    p.start()
    p.join(2)
    # print(re)

    if p.is_alive():
        print ("running... let's kill it...")
        p.terminate()
        p.join()
    
    for proc in jobs:
        proc.join()
    print(return_dict.values())





# import multiprocessing
# from os import getpid

# def worker(procnum):
#     print('I am number %d in process %d' % (procnum, getpid()))
#     return getpid()

# if __name__ == '__main__':
#     pool = multiprocessing.Pool(processes = 3)
#     # print(pool.map(worker, range(5)))
#     pool.start()
#     pool.join(1)
    
#     if pool.is_alive():
#         print("running... let's kill it...")
#         p.terminate()
#         p.join()
# # bar



# def bar():
#     fu = "ich bin raus"
#     for i in range(1):
#         print("Tick")
#         time.sleep(1)
#     return fu

# if __name__ == '__main__':
#     # Start bar as a process
#     p = multiprocessing.Process(target=bar)
#     pa = p.start()
    
#     # Wait for 10 seconds or until process finishes
#     pa= p.join(10)
#     print(pa)
#     print("hallo")
#     # If thread is still active
#     if p.is_alive():
#         print("running... let's kill it...")

#         # Terminate - may not work if process is stuck for good
#         p.terminate()
#         # OR Kill - will work for sure, no chance for process to finish nicely however
#         # p.kill()

#         p.join()

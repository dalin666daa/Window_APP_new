
def run():
    global count
    count = count + 1 
    print(f"run{count}")
    return
count = 0
if __name__ == "__main__":
     
    while True:
     run()
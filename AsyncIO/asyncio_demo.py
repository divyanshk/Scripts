import asyncio
import time

async def work(i: int) -> None:
    print(i, "I'm working")
    await asyncio.sleep(2)
    return

async def main():
    start = time.perf_counter()
    ret = await asyncio.gather(*(work(i) for i in range(3)))    
    print("Time spent running main: ", time.perf_counter() - start)


if __name__ == '__main__':
    asyncio.run(main())
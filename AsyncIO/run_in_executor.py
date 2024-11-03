import asyncio
import aiofiles
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

async def read_file(file_path):
    async with aiofiles.open(file_path, mode='r') as file:
        contents = await file.read()
        return contents

def transform_content(content):
    # Example transformation: simulate a time-consuming operation
    return content.upper()  # Replace this with your actual transformation logic

async def run_in_executor(executor, func, *args):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, func, *args)

async def main(file_paths, io_threads=4, transform_processes=4):
    # Read files concurrently with a specified number of I/O threads
    async with ThreadPoolExecutor(max_workers=io_threads) as io_executor:
        read_tasks = [run_in_executor(io_executor, read_file, file_path) for file_path in file_paths]
        contents = await asyncio.gather(*read_tasks)

    # Transform contents concurrently in a separate process pool
    with ProcessPoolExecutor(max_workers=transform_processes) as transform_executor:
        transform_tasks = [run_in_executor(transform_executor, transform_content, content) for content in contents]
        transformed_contents = await asyncio.gather(*transform_tasks)
    
    return transformed_contents

if __name__ == "__main__":
    # List of files to read from
    files_to_read = ['file1.txt', 'file2.txt', 'file3.txt']  # Add your file names here

    # Specify the number of threads for I/O and processes for transformations
    io_thread_count = 4          # Change this to your desired number of I/O threads
    transform_process_count = 4   # Change this to your desired number of transform processes

    # Running the main function
    results = asyncio.run(main(files_to_read, io_thread_count, transform_process_count))

    # Print the transformed results
    for i, content in enumerate(results):
        print(f"Transformed content of file {files_to_read[i]}:\n{content}\n")
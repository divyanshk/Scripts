import asyncio
import random
import time

# Simulated data loading function
async def load_data(batch_size):
    # Simulate a delay for loading data
    await asyncio.sleep(random.uniform(0.1, 0.5))
    # Generate some fake data
    return [random.randint(1, 100) for _ in range(batch_size)]

# Worker function to process data
async def worker(worker_id, queue):
    while True:
        # Wait for a data batch
        batch = await queue.get()
        
        if batch is None:  # Check for termination signal
            queue.task_done() # Indicate that the task is done
            break
        
        # Simulate processing time
        await asyncio.sleep(random.uniform(0.2, 1.0))
        
        # Process the data (just squaring the numbers for this example)
        processed = [x ** 2 for x in batch]
        print(f"Worker {worker_id} processed: {processed}")
        
        queue.task_done()  # Mark the task as done

# DataLoader that manages loading and distributing tasks
class DataLoader:
    def __init__(self, num_workers, batch_size, num_batches):
        self.queue = asyncio.Queue()
        self.num_workers = num_workers
        self.batch_size = batch_size
        self.num_batches = num_batches

    async def load_and_process(self):
        # Start worker tasks
        workers = [asyncio.create_task(worker(i, self.queue)) for i in range(self.num_workers)]

        # Load data in batches
        for _ in range(self.num_batches):
            batch = await load_data(self.batch_size)
            await self.queue.put(batch)

        # Stop workers
        for i in range(self.num_workers):
            await self.queue.put(None)  # Send termination signal to workers

        # Wait for all tasks to be done
        await self.queue.join()

        # Cancel workers
        for w in workers:
            w.cancel()

async def main():
    num_workers = 4
    batch_size = 5
    num_batches = 10

    data_loader = DataLoader(num_workers, batch_size, num_batches)
    await data_loader.load_and_process()

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
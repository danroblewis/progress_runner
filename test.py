import progress_runner
import random
import asyncio


async def custom_fn(num):
    await asyncio.sleep(random.random())
    return random.random() > 0.1


params = [ [i] for i in range(1000) ]
progress_runner.run(custom_fn, params)

# p = progress_runner.ProgressRunner(custom_fn, params)
# p.run()
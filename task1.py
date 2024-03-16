import argparse, asyncio, logging, os

from aiopath import AsyncPath
from aioshutil import copyfile


parser = argparse.ArgumentParser(description="Sorting files")
parser.add_argument("--source", "-s", required=True, help="Source dir")
parser.add_argument("--output", "-o", help="Destination dir", default="output folder")
args = vars(parser.parse_args())

source = AsyncPath(args["source"])
dest = AsyncPath(args["output"])

# source = AsyncPath("source")
# dest = AsyncPath("output")

copied_files = []

async def read_folder(path: AsyncPath):
    if os.path.exists(path):
        async for file in path.iterdir():
            if await file.is_dir():
                await read_folder(file)
            else:
                await copy_file(file)
    else:
        print(f"Folder {path} doesn't exist. List of files to copy is empty")

async def copy_file(file: AsyncPath):
    folder = dest / file.suffix[1:]
    new_file = file
    if folder / file.name in copied_files:
        s = len(file.name) - len(file.suffix)
        new_file = AsyncPath(file.name[0:s] + "_" + file.name[s:])
    try:
        await folder.mkdir(exist_ok=True, parents=True)
        copied_files.append(folder / file.name)
        await copyfile(file, folder / new_file.name)
    except OSError as e:
        logging.error(e)

if __name__ == "__main__":
    format = "%(threadName)s %(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    asyncio.run(read_folder(source))

    print(f"All files from '{source}' copied to '{dest}' folder")
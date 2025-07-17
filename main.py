from asyncio import run
from ingestion import ingestion_main
from load import load_main
from transform import transforms
import sys

async def main():
    if '--transform' in sys.argv:
        transforms()
    if '--ingestion' in sys.argv:
        await ingestion_main()
    if '--load' in sys.argv:
        await ingestion_main()
        load_main()
        transforms()
    if '--transform' in sys.argv and '--ingestion' in sys.argv:
        await ingestion_main()
        load_main()
        transforms()

if __name__ == "__main__":
    run(main())
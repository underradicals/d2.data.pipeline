from asyncio import run
from ingestion import ingestion_main
from load import load_main

async def main():
    await ingestion_main()
    load_main()

if __name__ == "__main__":
    run(main())
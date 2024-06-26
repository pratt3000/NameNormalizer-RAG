from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from db.crud import get_table_data, update_query_status

from src.internet_scraper import scrape
from src.constants import COLLECTION_NAME, EMBEDDINGS_SIZE
from src.qdrant_utils import get_embeddings, init_collection, upload_objlist_to_Qdrant
from tqdm import tqdm


# Function to scrape data and upload embeddings to Qdrant
def scrape_data_and_upload_embeddings_to_qdrant(table_data):
    company_names = [names + " company" for names in table_data]
    all_data = {}
    for company in company_names:
        print(f"Scraping data for {company}")

        # Scrape data for each company.
        company_details = scrape(company)

        # Append the query name to the entities list
        company_details["wiki_text"]["entities"].append(company.split(" ")[0])

        if company_details:
            all_data[company_details["company_name"]] = company_details

    # Upload embeddings to Qdrant
    print("UPLOADING EMBEDDINGS TO Qdrant")
    init_collection(
        COLLECTION_NAME, EMBEDDINGS_SIZE
    )  # only creates when index not already present
    for company in all_data:
        for alternative_merchant_name in tqdm(
            all_data[company]["wiki_text"]["entities"]
        ):
            # Get embeddings for each alternative name.
            embeddings = get_embeddings(alternative_merchant_name, company)

            # Upload embeddings to Qdrant
            upload_objlist_to_Qdrant(COLLECTION_NAME, embeddings)


# Check database for new queries and update embeddings in Qdrant for the new queries.
def update_job():
    from db.database import SessionLocal

    print("Job started")

    db_session: Session = SessionLocal()

    # Get all the table data from the database and prepare for scraping.
    table_names = get_table_data(db_session)
    table_data = []
    table_query_ids = []
    for table_name in table_names:
        table_data.append(table_name.query)
        table_query_ids.append(table_name.id)

    # scrape and upload data embeddings to Qdrant
    scrape_data_and_upload_embeddings_to_qdrant(table_data)

    # Update the status of processed queries.
    update_query_status(db_session, table_query_ids, status=False)

    print("Job finished")
    db_session.close()


def start_scheduler():
    hours_interval = 1  # Change this value to your desired interval

    # Create a scheduler instance
    scheduler = BackgroundScheduler()

    # Add the job to the scheduler. 'interval' triggers are used for running the job at regular intervals.
    scheduler.add_job(update_job, "interval", hours=hours_interval)

    # Start the scheduler
    scheduler.start()

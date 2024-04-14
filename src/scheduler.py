from apscheduler.schedulers.background import BackgroundScheduler
import datetime

from sqlalchemy.orm import Session
from db.crud import get_table_data, update_query_status

from src.internet_scraper import scrape
import json
from src.constants import INDEX_NAME, NAMESPACE
from src.pinecone_utils import get_index, get_embeddings, init_index
from tqdm import tqdm


def scrape_data_and_upload_embeddings_to_pinecone(table_data):
    # Scrape data
    company_names = [names + ' company' for names in table_data]
    all_data = {}
    for company in company_names:
        print(f"Scraping data for {company}")
        company_details = scrape(company)
        company_details['wiki_text']['entities'].append(company.split(' ')[0])
        if company_details:
            all_data[company_details['company_name']] = company_details
    

    # # Save to json
    # with open('company_data.json', 'w') as f:
    #     json.dump(all_data, f, indent=4)


    # Upload embeddings to Pinecone
    print("UPLOADING EMBEDDINGS TO Qdrant")
    init_index(INDEX_NAME) # only creates when index not already present
    merchant_index = get_index(INDEX_NAME)

    for company in all_data:
        for alternative_merchant_name in tqdm(all_data[company]['wiki_text']['entities']):
            embeddings = get_embeddings(
                alternative_merchant_name, company
            )  # Get embeddings for each alternative name
            merchant_index.upsert(
                vectors=embeddings, namespace=NAMESPACE
            )

    # Print index stats
    print(merchant_index.describe_index_stats())


def update_job():
    from db.database import SessionLocal
    print("Job started")

    db_session: Session = SessionLocal()
    
    table_names = get_table_data(db_session)
    table_data = []
    table_query_ids = []
    for table_name in table_names:
        table_data.append(table_name.query)
        table_query_ids.append(table_name.id)

    # scrape and upload data embeddings to Pinecone
    scrape_data_and_upload_embeddings_to_pinecone(table_data)
    
    update_query_status(db_session, table_query_ids, status = False)
    
    print("Job finished")
    db_session.close()


def start_scheduler():

    hours_interval = 1  # Change this value to your desired interval

    # Create a scheduler instance
    scheduler = BackgroundScheduler()

    # Add the job to the scheduler. 'interval' triggers are used for running the job at regular intervals.
    scheduler.add_job(update_job, 'interval', hours=hours_interval)

    # Start the scheduler
    scheduler.start()
from common.database.postgres.pool import postgres_db_pool
from common.models import Record


async def delete_record(record: Record):
    async with postgres_db_pool.get_db_connection() as conn:
        async with conn.transaction():
            # 1. delete from db
            await conn.execute(
                "DELETE FROM record WHERE collection_id=$1 AND record_id=$2;", record.collection_id, record.record_id
            )

            # 2. update collection num_records and num_chunks
            await conn.execute(
                "UPDATE collection "
                "SET num_records = num_records - 1, num_chunks = num_chunks - $1 "
                "WHERE collection_id=$2;",
                record.num_chunks,
                record.collection_id,
            )

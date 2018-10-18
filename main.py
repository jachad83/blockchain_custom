#!/usr/bin/python
import hashlib as hsh
import datetime as date
import psycopg2 as psy
import sys
from reader import file_capture


# define module variables / database config; could use a config file, i.e. config.ini
DBNAME = "blockchains"
DBUSER = "blockchains_user"
DBHOST = "localhost"
DBPASSWORD = "blockchains_pass"


# define block objects
class Block:
    def __init__(self, timestamp, data, previous_hash):
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self._hash_block()

    # create block hash
    def _hash_block(self):
        hash_string = "{}{}{}".format(self.timestamp, self.data, self.previous_hash)
        sha = hsh.md5(hash_string.encode()).hexdigest()

        return sha


# takes user input and creates / adds to blockchain table
def _blockchain_create(blockchain_name):
    _db_name = DBNAME
    _db_table = blockchain_name
    _db_user = DBUSER
    _db_host = DBHOST
    _db_password = DBPASSWORD

    # create a new data block
    def _new_block(data_, previous_block):
        this_timestamp = str(date.datetime.now())
        this_data = data_
        this_previous_hash = previous_block.hash

        return Block(this_timestamp, this_data, this_previous_hash)

    def _chain_create(genesis):
        file_data_list = file_capture()
        count = int(len(file_data_list))

        # iterate through blocks creation
        for _ in range(count):
            # initialise the blockchain
            if _ == 0:
                if genesis:
                    # start a new blockchain
                    blockchain = [Block(str(date.datetime.now()), "Genesis Block", "0")]
                    previous_block = blockchain[0]
                else:
                    # create blockchain to add to an existing table
                    try:
                        # fetch last block from existing blockchain table
                        # cur.execute("rollback;")
                        cur.execute("SELECT timestamp, data, previous_hash FROM {} ORDER BY id DESC limit 1;".format(_db_table))
                    except psy.Error as e:
                        cur.execute("rollback;")
                        cur.close()
                        conn.close()
                        print("Block retrieval failure: \n" +str(e))
                        sys.exit(1)
                    # use fetched block to create the first block of blockchain to be added to existing table
                    last_row = cur.fetchone()
                    blockchain = []
                    # fetched block is rehashed to keep data integrity
                    previous_block = Block(last_row[0], last_row[1], last_row[2])

            # add block to blockchain
            new_block_ = _new_block(file_data_list[_], previous_block)
            blockchain.append(new_block_)
            previous_block = new_block_

        return blockchain

    # interact with blockchain database table
    def _db_interaction(create_db):
        # create blocks to add to database table
        blockchain_ = _chain_create(create_db)
        # add blockchain blocks sequentially to blockchain database table
        for block in blockchain_:
            try:
                cur.execute("INSERT INTO {} (timestamp, data, previous_hash, hash) \
                    VALUES ('{}', '{}', '{}', '{}');".format(_db_table, block.timestamp, block.data, block.previous_hash, block.hash))
            except psy.Error as e:
                cur.execute("rollback;")
                cur.close()
                conn.close()
                print("Error adding block to blockchain table: " + block + "\n" + str(e))
                sys.exit(1)

        conn.commit()
        cur.close()
        conn.close()

    # try to connect to database
    try:
        conn = psy.connect(host=_db_host, database=_db_name, user=_db_user, password=_db_password)
        cur = conn.cursor()
    except psy.Error as e:
        print("Database connection failure: \n" + str(e))
        sys.exit(1)
    # try to create new blockchain table
    try:
        # blockchain table does not exist; is new blockchain
        cur.execute("CREATE TABLE {} (id serial PRIMARY KEY, timestamp varchar, \
            data varchar, previous_hash varchar, hash varchar);".format(_db_table))
        print("Blockchain not found; creating chain.")
        _db_interaction(True)
    except: # not an error so no exception class
        # blockchain table does exist; adding to existing blockchain
        cur.execute("rollback;")
        print("Blockchain found; adding to chain.")
        _db_interaction(False)


def main():
    # user prompt for blockchain name and number of blocks to add
    blockchain_name_input = input('Enter name of blockchain to create / add to: ')

    _blockchain_create(blockchain_name_input)


if __name__ == "__main__":
    main()

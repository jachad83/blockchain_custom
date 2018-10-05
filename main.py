#!/usr/bin/python
import hashlib as hsh
import datetime as date
import psycopg2 as psy
import random as rdm
import string as str_
import sys


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
        sha = hsh.sha256(hash_string.encode()).hexdigest()

        return sha


# takes user input and creates / adds to blockchain table
def blockchain_create(blockchain_name, block_count):
    # could use a config file, i.e. config.ini
    db_name = DBNAME
    db_table = blockchain_name
    db_user = DBUSER
    db_host = DBHOST
    db_password = DBPASSWORD

    # create a new data block
    def _new_block(previous_block):
        this_timestamp = str(date.datetime.now())
        this_data = ''.join(rdm.choices(str_.ascii_uppercase + str_.digits, k=30))
        this_hash = previous_block.hash

        return Block(this_timestamp, this_data, this_hash)

    def _chain_create(genesis):
        # iterate through blocks creation
        for _ in range(block_count):
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
                        cur.execute("rollback;")
                        cur.execute("SELECT timestamp, data, previous_hash FROM {} ORDER BY id DESC limit 1;".format(db_table))
                    except psy.DatabaseError as e:
                        print(e)
                        sys.exit(1)
                    # use fetched block to create the first block of blockchain to be added to existing table
                    last_row = cur.fetchone()
                    blockchain = []
                    # fetched block is rehashed to keep data integrity
                    previous_block = Block(last_row[0], last_row[1], last_row[2])

            # add block to blockchain
            new_block_ = _new_block(previous_block)
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
                    VALUES ('{}', '{}', '{}', '{}');".format(db_table, block.timestamp, block.data, block.previous_hash, block.hash))
            except Exception:
                print("Error adding block to blockchain table: "+block)
                sys.exit(1)

        conn.commit()

    # try to connect to database
    try:
        conn = psy.connect(host=db_host, database=db_name, user=db_user, password=db_password)
        cur = conn.cursor()
    except Exception:
        print("Database connection failure.")
        sys.exit(1)
    # try to create new blockchain table
    try:
        # blockchain table does not exist; is new blockchain
        cur.execute("CREATE TABLE {} (id serial PRIMARY KEY, timestamp varchar, \
            data varchar, previous_hash varchar, hash varchar);".format(db_table))
        print("Blockchain not found; creating chain.")
        _db_interaction(True)
    except Exception:
        # blockchain table does exist; adding to existing blockchain
        print("Blockchain found; adding to chain.")
        _db_interaction(False)


def main():
    # user prompt for blockchain name and number of blocks to add
    blockchain_name_input = input('Enter name of blockchain to create / add to: ')
    block_count_input = input('Enter number of blocks to add: ')

    # run
    blockchain_create(blockchain_name_input, int(block_count_input))


if __name__ == "__main__":
    main()

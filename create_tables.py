from main import db
from seed import example_data


if __name__ == '__main__':
    print('Creating all database tables...')
    db.drop_all()
    db.create_all()
    example_data()
    print('Done!')
# [END all]
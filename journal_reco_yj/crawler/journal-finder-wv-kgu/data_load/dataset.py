from data_load.wordvice_db import DB


class journalTitle:

    #create data to get authorguideline URL
<<<<<<< HEAD



    def create_journalTitle_dataset(row):
=======
    def create_journalTitle_dataset(self):

>>>>>>> e47389166fb72c60e91e692e945976515bef7041
        #get data from DB
        data = []
        temp = []

        while row is not None:
            if row == {}:
                break
            temp.append(row)
            row = DB.cur.fetchone()

        for item in temp:
            data.append(item['journalTitle'])

        print('create_journalTitle_dataset')
<<<<<<< HEAD
        return data
=======
        return dataset

# print(journalTitle.create_journalTitle_dataset(row))

>>>>>>> e47389166fb72c60e91e692e945976515bef7041

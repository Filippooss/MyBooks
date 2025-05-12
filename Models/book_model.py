class Book:
    def __init__(self,id,title,author,publisher,release_year,description,version,image_raw):
        self.id:int = id
        self.title:str = title
        self.author:str = author
        self.publisher:str = publisher
        self.release_year:int = release_year
        self.description:str = description
        self.version:int = version
        self.image_raw:bytes = image_raw

    #https://stackoverflow.com/questions/1436703/what-is-the-difference-between-str-and-repr
    def __repr__(self):
        return (f"Book(id = {self.id},title = {self.title}, author = {self.author}, publisher = {self.publisher}, release year = {self.release_year}",
                f"description = {self.description}, version = {self.version}, image = {self.image_raw}"
            )

        

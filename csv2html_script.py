import csv

if __name__ == "__main__":
    
    message = ""
    with open("df_sorted_no_dups.csv", "r") as csv_file:
        reader = csv.DictReader(csv_file)
        i = 1
        for row in reader:
            temp = str(i)+ "<p><b> </b><b>Name -</b> {name}, <b>Rating -</b> {rating}, <b>No. of Reviews -</b> {no_of_reviews}, <b>Popularity -</b> {popularity}</p>".format(
                name=row["name"],
                rating=row["rating"],
                no_of_reviews=row["no_of_reviews"],
                popularity=row["popularity"]
            )
            temp += '<img src="{source}"/>'.format(source=row["img_links"])
            temp = "<div>" + temp + "</div>"
            message += temp
            i+=1
        
    message = "<html><body><style> div { margin: 5px } img { width : 200px; height: 200px; }</style>" + message + "</body></html>"
    
    with open("output.html", "w") as output_file:
        output_file.write(message)
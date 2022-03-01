import shapefile
import yaml

# get configs from shapefile_configs
with open('shapefiles/shapefile_configs.yml', 'r') as file:
    configs = yaml.safe_load(file)

# temporarily store record data here -> later we'll have to write this to shapefiles.
# right now I'm keeping it simple
record_array = []

# iterate through the counties for which we have data (all our shapefiles)
for county in configs["counties"]:
    # pull filename from configs and open shapefile
    filename = configs["counties"][county]["filename"]
    sf = shapefile.Reader(f"shapefiles/{filename}")
    # we can see all the fields in the shapefile by running:
    # print(sf.fields)

    # this is just to show you a bit more about how we're pulling data from the config files
    # it'll print a out what each required_field is labelled in the county's shapefile
    # we do this again below but I don't wanna print it out a thousand times
    for field in configs["required_fields"]:
        field_in_file = configs["counties"][county][field]
        print(f"the {field} field is labelled {field_in_file} for {county}'s data.")
    print("")
    
    # we can iterate through the records in the shapefile
    for record in sf.records():
        # go through required fields and find them based on county specifications
        # right now we're just creating tuples with the data so that we can see the
        # relevant data that we're pulling. later we'll write all of em to a new shapefile
        record_item = []
        for field in configs["required_fields"]:
            field_in_file = configs["counties"][county][field]
            record_item.append((field, record[field_in_file]))
        record_item.append(('county', county))
        record_array.append(tuple(record_item))

# now we can print all our records from our array
print("\n".join(str(r) for r in record_array))

# to see what this code outputs, check out the sample_output.txt file :)
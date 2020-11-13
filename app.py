from flask import Flask, request, render_template
from PIL import Image, ImageFilter
from pprint import PrettyPrinter
import json
import os
import random
import requests

app = Flask(__name__)

@app.route('/')
def homepage():
    """A homepage with handy links for your convenience."""
    return render_template('home.html')

################################################################################
# COMPLIMENTS ROUTES
################################################################################

list_of_compliments = [
    'awesome',
    'beatific',
    'blithesome',
    'conscientious',
    'coruscant',
    'erudite',
    'exquisite',
    'fabulous',
    'fantastic',
    'gorgeous',
    'indubitable',
    'ineffable',
    'magnificent',
    'outstanding',
    'propitioius',
    'remarkable',
    'spectacular',
    'splendiferous',
    'stupendous',
    'super',
    'upbeat',
    'wondrous',
    'zoetic'
]

@app.route('/compliments')
def compliments():
    """Shows the user a form to get compliments."""
    return render_template('compliments_form.html')

@app.route('/compliments_results')
def compliments_results():
    """Show the user some compliments."""

    users_name = request.args.get('users_name')
    wants_compliments = request.args.get('wants_compliments')
    num_compliments = int(request.args.get('num_compliments'))
    result = ""

    if wants_compliments == "yes":
        result = random.sample(list_of_compliments, num_compliments)

    if wants_compliments == "no":
        result = "not wanting compliments"

    context = {
        'users_name' : users_name,
        'wants_compliments' : wants_compliments,
        'num_compliments' : num_compliments,
        'result' : result
    }

    # print(users_name)
    # print(wants_compliments)
    # print(num_compliments)
    # print(result)
    return render_template('compliments_results.html', **context)


################################################################################
# ANIMAL FACTS ROUTE
################################################################################

animal_to_fact = {
    'koala': 'Koala fingerprints are so close to humans\' that they could taint crime scenes.',
    'parrot': 'Parrots will selflessly help each other out.',
    'mantis_shrimp': 'The mantis shrimp has the world\'s fastest punch.',
    'lion': 'Female lions do 90 percent of the hunting.',
    'narwhal': 'Narwhal tusks are really an "inside out" tooth.'
}

@app.route('/animal_facts')
def animal_facts():
    """Show a form to choose an animal and receive facts."""

    animal = ""
    animal_result = ""

    # TODO: Collect the form data and save as variables
    animal = request.args.get('animal')
    animal_result = request.args.get('animal_result')

    koala = animal_to_fact["koala"]
    parrot = animal_to_fact["parrot"]
    mantis_shrimp = animal_to_fact["mantis_shrimp"]
    lion = animal_to_fact["lion"]
    narwhal = animal_to_fact["narwhal"]

    if animal == 'koala':
        animal_result = animal_to_fact["koala"]
    elif animal == 'parrot':
        animal_result = animal_to_fact["parrot"]
    elif animal == 'mantis_shrimp':
        animal_result = animal_to_fact["mantis_shrimp"]
    elif animal == 'lion':
        animal_result = animal_to_fact["lion"]
    elif animal == 'narwhal':
        animal_result = animal_to_fact["narwhal"]
    
    # print(animal_result)

    context = {
        # TODO: Enter your context variables here for:
        # - the list of all animals (get from animal_to_fact)
        # - the chosen animal fact (may be None if the user hasn't filled out the form yet)
        'koala' : koala,
        'parrot' : parrot,
        'mantis_shrimp' : mantis_shrimp,
        'lion' : lion,
        'narwhal' : narwhal,
        'animal' : animal,
        'animal_result' : animal_result
    }

    return render_template('animal_facts.html', **context)


################################################################################
# IMAGE FILTER ROUTE
################################################################################

filter_types_dict = {
    'blur': ImageFilter.BLUR,
    'contour': ImageFilter.CONTOUR,
    'detail': ImageFilter.DETAIL,
    'edge enhance': ImageFilter.EDGE_ENHANCE,
    'emboss': ImageFilter.EMBOSS,
    'sharpen': ImageFilter.SHARPEN,
    'smooth': ImageFilter.SMOOTH
}

def save_image(image, filter_type):
    """Save the image, then return the full file path of the saved image."""
    # Append the filter type at the beginning (in case the user wants to 
    # apply multiple filters to 1 image, there won't be a name conflict)
    new_file_name = f"{filter_type}-{image.filename}"
    # space_filter = string.split[' '] = '-' for loop, append into -
    image.filename = new_file_name

    # Construct full file path
    file_path = os.path.join(app.root_path, 'static/images', new_file_name)
    
    # Save the image
    image.save(file_path)

    return file_path


def apply_filter(file_path, filter_name):
    """Apply a Pillow filter to a saved image."""
    i = Image.open(file_path)
    i.thumbnail((500, 500))
    i = i.filter(filter_types_dict.get(filter_name))
    i.save(file_path)

@app.route('/image_filter', methods=['GET', 'POST'])
def image_filter():
    """Filter an image uploaded by the user, using the Pillow library."""
    filter_types = filter_types_dict.keys()

    if request.method == 'POST':
        
        # TODO: Get the user's chosen filter type (whichever one they chose in the form) and save
        # as a variable
        filter_type = request.form.get('filter_type')
        
        # Get the image file submitted by the user
        image = request.files.get('users_image')

        # TODO: call `save_image()` on the image & the user's chosen filter type, save the returned
        # value as the new file path
        file_path = save_image(image, filter_type)
        # print(save_image(image, filter_type))

        # TODO: Call `apply_filter()` on the file path & filter type
        apply_filter(file_path, filter_type)
        image_url = f'/static/images/{image.filename}'
        # image_url = file_path

        context = {
            # TODO: Add context variables here for:
            # - The full list of filter types
            # - The image URL
            'filter_types' : filter_types,
            'image' : image,
            'file_path' : file_path,
            'image_url' : image_url,
        }

        return render_template('image_filter.html', **context)

    else: # if it's a GET request

        # filter_types = filter_types_dict.keys()
        
        # filter_type = request.form.get('filter_type')
        # image = request.files.get('users_image')

        # file_path = save_image(image, filter_type)

        # apply_filter(file_path, filter_type)
        # image_url = f'/static/images/{image.filename}'

        context = {
            # 'filter_types' : filter_types,
            # 'image' : image,
            # 'file_path' : file_path,
            # 'image_url' : image_url
        }

    return render_template('image_filter.html', **context)





################################################################################
# GIF SEARCH ROUTE
################################################################################

API_KEY = 'LIVDSRZULELA'
TENOR_URL = 'https://api.tenor.com/v1/search'
pp = PrettyPrinter(indent=4)

@app.route('/gif_search', methods=['GET', 'POST'])
def gif_search():
    
    """Show a form to search for GIFs and show resulting GIFs from Tenor API."""
    if request.method == 'POST':
        # TODO: Get the search query & number of GIFs requested by the user, store each as a 
        # variable
        q = request.form.get('search_query')
        limit = request.form.get('quantity')

        response = requests.get(
            TENOR_URL,
            {
                'q' : q,
                'key' : API_KEY,
                'limit' : limit
                # TODO: Add in key-value pairs for:
                # - 'q': the search query
                # - 'key': the API key (defined above)
                # - 'limit': the number of GIFs requested
            })

        gifs = json.loads(response.content).get('results')

        context = {
            'gifs': gifs,
        }

        # Uncomment me to see the result JSON!
        pp.pprint(gifs)

        return render_template('gif_search.html', **context)
    else:


        return render_template('gif_search.html')

if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.run(debug=True)
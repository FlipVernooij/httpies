# httpies
Like HTTPIE?, you will love this! (https://github.com/httpie/httpie)

# Script, save & share
Create a script that generates the parameters for your httpie request, store it in your repository and allow you and your team-mates to (re)use it.
By storing these files in a url-like directory structure, you can simply call an url, overwrite some custom params and request your response.

In some way, it's a terminal based postman-like implementation that offers much much more flexibillaty in a very simple way.

# Prepare your repository
- create the directory-layout for httpies
    - \[your_repo\]/httpies
        - urls
- Add the httpies directy to your environment variables.
    echo  "export HTTPIES_BASEDIR='\[your_repo\]/httpies'" >> ~/.zshrc (or .bashrc)
    
- Set the default domain to be passed with every request.    
    echo  "export HTTPIES_DEFAULT_DOMAIN='https://www.yourdomain.com'" >> ~/.zshrc (or .bashrc)

# Write your url-script file
    \[BASE_DIR\]/user/get.py:

    import argparse
    arg_parser = argparse.ArgumentParser()
    # These arguments are always passed to your script from the httpies command, you are free to bluntly ignore them, yet they might prove useful.
    arg_parser.add_argument('_method')
    arg_parser.add_argument('_domain')
    arg_parser.add_argument('_url')

    # You can add as much custom arguments to your script, best practive it to make them optional with a default value.
    arg_parser.add_argument('-u', '--username', default="test@username.com", help="Custom argument for this script, add as many as you like.")

    # Parameters passed to httpie, 1 per line
    # @see https://github.com/httpie/httpie for details and documentation.
    print(args._method)
    print('%s%s' (args.domain,args.url))
    print('X-customHeader: my header')
    print('username==%s', args.username)
    print('--json')
    print('--verbose')
    sys.exit(0)

# Execute your request
    https get /user -u "flip@github.com"
It is as simple as that,.. enjoy the response.
  
# Supported extensions:

  In the config-file there are some extension mappings.
  You can add any extension you want to the configfile, just add the required executable with it.
  By default the following extensions will be reconized:
  
  - .py  (python)
  - .php (php)
  - .rb  (ruby)
  - .js  (node)
  - .bsh (bash)
  - .sh  (sh)
  
## Adding a new extension to the config-file.
    \[executables\]
    py = python
    hp = php
    js = node
    rb = ruby
    sh = sh
    bsh = bash
    \{YOUR_EXTENSION\} = {YOUR_EXECUTABLE}


# Files without a extension
By default htties will make these files executable (you can disable this in the config) and will try to execute them in order to receive the response.
This means you can use any type of executable with httpies as long as they return a proper response to the stdout.

# todo
This is a first version and aldue working there are quite some improvements I would like to add:

- general testing
- Passing arguments to your scriptfiles might be improved for other languages than python.
- Allow testing, perhaps use a ".after" or ".test" extension allowing you to write tests based on the httpie response.
- Test OSX and Windows, I am reasonably confident it will run on osX, yet I am just as confident that it won't run on windows.

# httpies
Like HTTPIE (https://github.com/httpie/httpie)?, you will love this!

# Script, save & share
Create a script that generates the parameters for your httpie request, store it in your repository and allow your team-mates to use it.
By storing these scipt file in a url-like directory structure, you can simply call your url, add some custom params and request your response.

# Write your url-script file
    \[BASE_DIR\]/user/get.py:

    import argparse
    arg_parser = argparse.ArgumentParser(description="url-script file providing parameters to my httpie request")
    arg_parser.add_argument('_method', help="Automaticly passed")
    arg_parser.add_argument('_domain', help="Automaticly passed")
    arg_parser.add_argument('_url', help="Automaticly passed")

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
    https get /user -u="flip@github.com"
It is as simple as that.
  
# Supported extensions:

  Litterly anything that you manage to execute on your machine!
  In the config-file there are some extension mappings, yet if you leave out the extension.. httpies will simple execute your file and use its response.
  By default the following extensions will be reconized:
  
  - .py  (python)
  - .php (php)
  - .rb  (ruby)
  - .js  (node)
  - .bsh (bash)
  - .sh  (sh)

But you can add any extension you want to the config file.

# Files without a extension
By default htties will make these files executable (you can disable that in the config) and will try to execute them in order to receive the response.

# todo
This is a first version and aldue working there are quite some improvements I would like to add:

- Config file should be places in the base dir/repo dir so it is shared together with the url-scripts.
- Passing arguments to your scriptfiles might be improved for other languages than python.
- Allow testing, perhaps use a ".after" or ".test" extension allowing you to write tests based on the httpie response.
- Test osX and Windows, I am reasonably confident that it will run on osX, yet I am just as confident that it won't run on windows.

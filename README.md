# httpies
Httpies is a wrapper around [httpie](https://httpie.io/) that allows you script your http request in order to test your api's.
It allows you to store these scripts along with your api code within your repository, making sharing and re-using fairly easy.
By passing all custom command-line arguments to your script, you can overwrite preset form values and make your scripts as dynamic as you want.


## Script, save & share
Use your favorite scripting language for your scripts, as httpies supports anything you can wish for.
Simply save your script(s) preferably mimicking the url structure of your api and make it part of your repository.
You and your team-mates can call your script(s), overwrite parameters and verify responses.

In some way, it's a terminal based postman-like implementation that offers much much more flexibility in a very simple way.

# Getting it to work.
## Prepare your repository
- create the directory-layout for httpies
    - \[your_repo\]/httpies
        - urls
- Add the httpies directory to your environment variables.
    
      echo  "export HTTPIES_BASEDIR='\[your_repo\]/httpies'" >> ~/.zshrc (or .bashrc)
    
- Set the default domain to be passed with every request.    
    
      echo  "export HTTPIES_DEFAULT_DOMAIN='https://www.yourdomain.com'" >> ~/.zshrc (or .bashrc)

## Write your url-script file
Out of the box httpies supports .py (python), .php (php), .rb (ruby), .js (node), .sh (sh), .bsh (bash).
Yet you are free to add any extension to the config file.
Check the [httpies documentation](https://httpie.io/docs)

### Python example
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

### PHP example
     \[BASE_DIR\]/user/get.php:
    <?php
    # default arguments that are always supplied
    $method = $argv[1];
    $domain = $argv[2];
    $url = $argv[3];
    
    # set my default arguments
    $args = [
        'username' => 'default@example.com',
    ];
    # parse the left-over arguments and append/overwrite them to the $args array.
    if(count($argv) > 3){
        for($i=4;$i<count($argv);$i++){
            $t = explode('=', $argv[$i], 2);
            $args[str_replace('--', '', $t[0])] = $t[1];
        }
    }
    # echo the httpies parameters.
    echo strtoupper($method) . "\n";
    echo $domain . $url . "\n";
    echo "X-customHeader: my header \n";
    echo "username==" . $args['username'] . "\n";
    echo "--json \n";
    echo "--verbose \n";
    echo "username==" . $args['username'] . "\n";
    exit(0);    

### sh Example
    \[BASE_DIR\]/user/get.sh
    $username="default@example.com"
    
    # Parse the arguments, 
    ## --username=flip@github.com will create the variable $username=flip@github.com
    for((i=0;i<=$#;i++));
        do
            arg="${!i}";
            if [[ $arg == --* ]]
                then
                    full=${arg#??};
                    eval $full;
            fi
        done
    
    cat << EOF
        $1
        $2$3
        username==$username
        --json
        --verbose
    EOF

    
## Execute your request
    https get /user --username="flip@github.com"
It is as simple as that,.. enjoy the response.
  
# Supported extensions:

 In the config-file there are some extension mappings.
 You can add any extension you want to the configfile, just add the required executable with it.
 By default the following extensions will be recognized:
  
  - .py  (python)
  - .php (php)
  - .rb  (ruby)
  - .js  (node)
  - .bsh (bash)
  - .sh  (sh)
  
## Adding a new extension.
Create an empty an empty config file in your basedir:
    touch [BASE_DIR]/httpies.conf
    
Then add the following entry:    
    \[executables\]
    py = python
    hp = php
    js = node
    rb = ruby
    sh = sh
    bsh = bash
    \{YOUR_EXTENSION\} = {YOUR_EXECUTABLE}

# Config files

By default, httpies works out of the box for most users.
Yet you might have specific wishes for one of your projects.
You can find the configfile that is used by running

    https -v20 get /test
    
The request will most probably end with an error, yet it will show you the currently used configfile at the first line of output.
You can either copy this file to your basedir, or just duplicated the required entries.
When httpies is executed, it first reads it's own config and will overwrite it with the properties found in your own config that resides in your \[base_dir\]

# Files without a extension
By default htties will make these files executable (you can disable this in the config) and will try to execute them in order to receive the response.
This means you can use any type of executable with httpies as long as they return a proper response to the stdout.

# todo
This is a first version and aldue working there are quite some improvements I would like to add:

- general testing

- Allow testing, perhaps use a ".after" or ".test" extension allowing you to write tests based on the httpie response.
- Passing arguments to your script-files might be improved for other languages than python.
- Test OSX and Windows, I am reasonably confident it will run on OSX, and just as confident that it won't run on windows.



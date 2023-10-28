# compai
A CLI for pair programming (or whatever other creative uses you can give it!) powered by AI.

The CLI currently uses the [Google Generative AI APIs](https://makersuite.google.com/), from here on referred to as PaLM.

## Installation
The tool is available as a [python package](https://pypi.org/project/compaipair/).

Install via pip:
```shell
pip install compaipair
```
Once installed the package will install a `compai` script that serves as entry point to the CLI.

## Configuration

### Cache directory
In order to access the API-key and use persisted data, like prompt templates, the package will create a directory 
`.compai` on your home directory.

You can change the default location of this directory by setting the environment variable `COMPAI_CACHE_PATH` to a different location.

### Configuring the PaLM API key
Since the CLI relies on the PaLM APIs you need an API key, which you can get [here](https://makersuite.google.com/), it will need to be accessed by the CLI when it's executed.

Currently, there are two ways to access the API key:
1. Via an `api_key` file
2. Via environment variables

#### Storing your API-key using the `init` command
Once the package is installed you can run the `init` command with your api key: 
```shell
complete init --api-key "<your api key>"
```
The package will create the directory `~/.compai` in your home-directory, where it will store your API-key in a file called `api_key`.


#### Storing your API-key in an environment variable
Alternatively, you can save your API-key in the environment variable `GOOGLE_GENERATIVEAI_API_KEY`.

#### **CAUTION:** 

The file is saved as plain text, and it's not encrypted or anything like that! Use at your own discretion, in an environment you trust!

## Usage

In order to explore the CLI, you can 
```shell
# Run the script with no arguments
compai
# Or with the --help option
compai --help
```
### Essential commands
The CLI exposes a few commands to prompt one of the Google Generative AI models:

#### `complete` 

Usage: `compai complete [OPTIONS] QUESTION`

This command prompts the user for a **question**, and uses the PaLM APIs to generate completions for the question. The completions are written to a file specified by the `-o` or `--output` flag.

The following options are available:

* `--priming`: A string to prime the LLM prompt.
* `--decorator`: A decorator to add to the prompt.
* `-o`, `--output`: The file to write the completions to.
* `-i`, `--input-file`: A file with input to append to the question.
* `-t`, `--temperature`: The model temperature, use 0 for more deterministic completions.
* `-m`, `--model-name`: The name of the LLM model to use.
* `-v`, `--verbose`: If set, includes the prompt in the output.
* `--plain-text`: Flag to output the results in plain text, otherwise will be formatted as Markdown.
* `--template`: A template to prime and decorate the prompt.

#### `complete-template`

Usage: `compai complete-template [OPTIONS] TEMPLATE`

This command prompts the user for a **template**,  and uses the PaLM APIs to generate completions for the question. The completions are written to a file specified by the `-o` or `--output` flag.

The following options are available:

* `-q`, `--question`: An optional question that will be appended to the template.
* `-o`, `--output`: The file to write the completions to.
* `-i`, `--input-file`: A file with input to append to the question.
* `-t`, `--temperature`: The model temperature, use 0 for more deterministic completions.
* `-m`, `--model-name`: The name of the LLM model to use.
* `-v`, `--verbose`: Whether to include the prompt in the output.
* `--plain-text`: Whether to print the output in plain text, or format it as Markdown.

#### `templates new`

Usage: `compai templates new [OPTIONS] NAME`

Creates a new template with priming and decorators

Options:
* `-p`, `--priming`:    Text for priming this template's prompts
* `-d`, `--decorator`:  Text for decorating this template's prompts

#### `templates edit`

Usage: `compai complete-template [OPTIONS] TEMPLATE`

Edit an existing template.

Options:
* `-q`, `--question` Optional question that will be appended to the template.
* `-o`, `--output` File to write output
* `-i`, `--input-file` File with input to append to the question.
* `-t`, `--temperature` Model temperature, use 0 for more deterministic completions.
* `-m`, `--model-name` LLM model for this query
* `-v`, `--verbose` Verbose. Include prompt in output
* `--plain-text` Print output in plain text, otherwise will be formatted as Markdown

#### `templates show`

Usage: `compai templates show [OPTIONS]`

Show the list of available templates.

`-n`, `--name` Name of the template to show.
`-v`, `--verbose` Show all the templates' contents
`--help` Show this message and exit.

## Example

Say you want to use an LLM to help you with your documentation. 
You could install `compai` and use it on your terminal next to your code editor to easily prompt an LLM. 
You can then prompt the LLM with code from your own codebase and write the results to a file on your disk.

### Simple usage
Let's see a simple example. I'm going to use code from this package, for instance the class `CompaiCompletion`:

```python
# ./compaipair/types/compaicompletion.py
# imports and preamble...
class CompaiCompletion:
    model: Model
    priming: str
    question: str
    decorator: str
    result: Completion
    api_key: str
    template: CompletionTemplate | None

    def __init__(
        self,
        model: Model | str,
        template: str = None,
        question: str = "",
        priming: str = "",
        decorator: str = "",
        temperature: float = 0.7,
        api_key: str = None,
    ):
        self.temperature = temperature

        self.question = question
        if template is None:
            self.priming = priming
            self.decorator = decorator
        if template is not None:
            template = CompletionTemplate.find_template(template)
            self.priming = template.priming if template.priming else priming
            self.decorator = template.decorator if template.decorator else decorator

        if api_key is None:
            self.api_key = get_api_key()

        configure_palm_api(api_key=self.api_key)

        if isinstance(model, Model):
            self.model = model
        elif model is None:
            self.model = self.get_model()
        else:
            self.model = self.get_model(model)

    def complete(self) -> Completion:
        self.result = palm.generate_text(
            prompt=self.prompt, model=self.model, temperature=self.temperature
        )
        return self.result
# ...more code
```

I'm going to use compai to generate docstrings for this class:

```shell
# cd "/../compaipair_dir"
compai complete "Can you generate docstrings for the following python class?" -i ./compaipair/types/compaicompletion.py
```
From this I just got the following (just a part of the output):
```python
class CompaiCompletion:                                                           
                                                                                   
     """                                                                           
     Class to generate text completions using the Palm API.                        
                                                                                   
     Args:                                                                         
         model (Model | str): The model to use for completion. If a string is      
             provided, it will be used to select a model from the list of          
             available models. If None, the default model will be used.            
         template (str | CompletionTemplate | None): The template to use for       
             generating the completion prompt. If a string is provided, it will    
             be used to find a template by name. If None, the default template     
             will be used.                                                         
         question (str): The question to be completed.                             
         priming (str): The priming text to be used before the question.           
         decorator (str): The decorator text to be used after the question.        
         temperature (float): The temperature to use for completion.               
         api_key (str): The API key to use for the Palm API. If None, the          
             default API key will be used.                                         
     """ 
# ...
```
It's important to always check what the model does, in this case the explanation of the argument `template` is not quite 
right, because I know (because I wrote the code) that if no template is provided, then the CLI just prepends and appends the priming and decorators, respectively.
Apart from that the result is kind of reasonable.

### Priming and decorating your prompts

Sometimes, priming or decorating your prompts might improve the quality of the results.

Let's use priming and decorators and see if we get a different result.

For priming, I'll use: "You're an experienced Python programmer who writes excellent documentation".
For a decorator, I'll tell the model to also comment the code and provide an explanation for the code.

```shell 
# cd "/../compaipair_dir"
compai complete --priming "You're an experienced Python programmer who writes excellent documentation."\
 --decorator "Please additionally provide a detailed explanation of what the code does."\
 "Can you generate docstrings and comments for the following python class?" -i ./compaipair/types/compaicompletion.py
```
In this case the result included docstrings for the class as well as a brief explanation of the class below.

> The CompaiCompletion class is a Python class for generating completions using the  
Palm API. It takes a number of arguments, including the model to use, the          
completion template to use, the question to generate completions for, the priming  
text to use, the decorator text to use, and the temperature to use for the         
completion.  

### Using templates

In your work, you might use different languages, or you might want to prompt the model for different purposes.
Templates provide a bit of convenience for these cases. They allow you to save primings and decorators that can be retrieved
for new questions you might ask an LLM. 

In the previous example we were working with python and producing docstrings. We could create a template `python-doc` 
that we can use whenever we want to produce documentation for python code:

```shell
compai templates new python-doc --priming "You're an experienced Python programmer who writes excellent documentation." \
--decorator "Please write docstrings for the preceding code."
# Check that the template was saved
compai templates show
```

The templates are saved as documents in a TinyDB database that lives in the cache directory, by default located
at `~/.compai/db.json`.

You can now use your template like this:

```shell
compai complete-template python-doc -i ./compaipair/types/compaicompletion.py
```
The output in this case looks very similar to the case above.

Let's say you're also working on a spring boot project with Kotlin and you want to generate test cases for your web
controllers. You could then save another template:

```shell
compai templates new kotlin-springboot-test --priming "You are an experienced Kotlin programmer with vast experience in the Spring Boot framework. Please generate test cases for the following code" --decorator "Please explain what each test case is supposed to test and write comments for your code"
```
And use it with the following code.

```kotlin
// ./spring-boot-project/UsersController.kt
@RestController
@RequestMapping("/users")
@CrossOrigin(origins = ["http://localhost:3000"])
class UsersController(private val usersRepository: UsersRepository, private val usersService: UsersService) {
    @GetMapping
    fun getUsers(): List<User> = usersRepository.findAll()

    @GetMapping("{id}")
    fun getUserById(@PathVariable id: String) = usersRepository.findById(id)

    @GetMapping("/email_or_username/")
    fun getUsersByUsernameOrEmail(@RequestParam term: String): List<User> =
        usersService.findUsersByUsernameOrEmail(term)
}
```

```shell
# cd ./spring-boot-project
compai complete-template kotlin-springboot-test -i UsersControllers.kt 
```
If it's some code from somewhere else that you can just copy-paste, you could use the `-q` or `--question` option to paste the code to the command:

```shell
compai complete-template kotlin-springboot-test -q '@RestController
@RequestMapping("/users")
@CrossOrigin(origins = ["http://localhost:3000"])
class UsersController(private val usersRepository: UsersRepository, private val usersService: UsersService) {
    @GetMapping
    fun getUsers(): List<User> = usersRepository.findAll()

    @GetMapping("{id}")
    fun getUserById(@PathVariable id: String) = usersRepository.findById(id)

    @GetMapping("/email_or_username/")
    fun getUsersByUsernameOrEmail(@RequestParam term: String): List<User> =
        usersService.findUsersByUsernameOrEmail(term)
}' 
```

In  this case this was the result (which hasn't been tested at all!!):

```kotlin
package com.example.demo.controller

import com.example.demo.model.User
import com.example.demo.repository.UsersRepository
import com.example.demo.service.UsersService
import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.extension.ExtendWith
import org.mockito.Mock
import org.mockito.Mockito.`when`
import org.mockito.junit.jupiter.MockitoExtension
import java.util.*

@ExtendWith(MockitoExtension::class)
class UsersControllerTest {

    @Mock
    private lateinit var usersRepository: UsersRepository

    @Mock
    private lateinit var usersService: UsersService

    @Test
    fun `getUsers returns all users`() {
        // Given
        val users = listOf(
            User(1, "John Doe", "john.doe@example.com"),
            User(2, "Jane Doe", "jane.doe@example.com")
        )
        `when`(usersRepository.findAll()).thenReturn(users)

        // When
        val result = UsersController(usersRepository, usersService).getUsers()

        // Then
        assertEquals(users, result)
    }

    @Test
    fun `getUserById returns the user with the given id`() {
        // Given
        val id = "1"
        val user = User(1, "John Doe", "john.doe@example.com")
        `when`(usersRepository.findById(id)).thenReturn(Optional.of(user))

        // When
        val result = UsersController(usersRepository, usersService).getUserById(id)

        // Then
        assertEquals(user, result)
    }

    @Test
    fun `getUsersByUsernameOrEmail returns the users with the given username or email`() {
        // Given
        val term = "john.doe"
        val users = listOf(
            User(1, "John Doe", "john.doe@example.com"),
            User(2, "Jane Doe", "jane.doe@example.com")
        )
        `when`(usersService.findUsersByUsernameOrEmail(term)).thenReturn(users)

        // When
        val result = UsersController(usersRepository, usersService).getUsersByUsernameOrEmail(term)

        // Then
        assertEquals(users, result)
    }
}
```

## Disclaimer

This is a personal project designed according to my taste and needs! Further development and maintenance of the project 
is subject to my time constraints.

Also, LLMs often hallucinate, so please check and test **everything** you get from an LLM.





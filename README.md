<pre>
    ▄███▀          ▄█                          ▄█                           ▀██▄
   ██▌             ▀▀                          ▀▀                             ▐██
   ██      ▄▄██▄▄▄ ▄▄   ▄▄██▄▄▄ ▄▄▄██▄▄  ▄▄  ▄▄▄▄▄  ▄█▄▄▄    ▄█▄▄  ▄▄▄ ▄▄█▄    ██
   ██    ▄██▀ ▀██▌ █▌ ▄██▀ ▀██▌ ▀▀▀  ▀██ ██    ▀█ ██  ▀▀█ ▄██▀ ▀██▄ ███▀▀▀██   ██
  ██▀    ██    ▐█▌ █▌ ██    ▐█▌      ▄██       ▐█ ██      ██     ██ █▌    ██   ▀██▄
▀█▄      ██    ▐█▌ █▌ ██    ▐█▌ ▄███▀▀██       ▐█  ▀███▄  ██     ██ █▌    ▐█▌    ▄██▀
  ██▄    ██    ▐█▌ █▌ ██    ▐█▌ █▌    ▐█       ▐█     ▀██ ██     ██ █▌    ▐█▌  ▄██▀
   ██    ▀██▄▄███▌ █▌ ▀██▄▄███▌ ██   ▄██ ██    ▐█ █▄  ▄██ ▐██▄ ▄██▀ █▌    ▐█▌  ██
   ██      ▀▀▀ ▐█▌ █▌   ▀▀▀ ▐█▌ ▀▀███▀▐█ ▀▀    ▐█ ▀▀██▀▀    ▀▀█▀▀   █▌    ▐█▌  ██
   ██▌   ▄▄    ██     ▄▄    ██            ▄▄   ▐█                             ▄██
    ▀▀██▄ ▀████▀       ▀████▀              ▀████▀                           ▄██▀
</pre>

## What is it?
I think actions speak louder than words, so let's start with some real examples to get your attention.

```python
>>> import giga_json as json
>>> from datetime import datetime
>>> 
>>> some_dict = {'timestamp': datetime.now()}
>>> 
>>> print(json.dumps(some_dict))
{
    "timestamp": "2023-11-03T15:17:00.148109"
}
```

That's what we wish the standard json.dumps() would do out of the box, right?  Well keep reading, as there's more:

```python
>>> import giga_json as json
>>> import requests
>>> 
>>> response = requests.get('https://catfact.ninja/fact')
>>> 
>>> print(json.dumps(response))
{
    "fact": "The most popular pedigreed cat is the Persian cat, followed by the Main Coon cat and the Siamese cat.",
    "length": 101
}
```

Cool, right?  You will struggle to find things that giga_json will fail to serialize, especially for Python's most commonly used objects. 

As long as you do the import like this: `import giga_json as json`, it will be a drop-in replacement for the standard json module.  If for some reason you need to access the standard dumps() method, you can use the convenience alias: `og_dumps()`:

```python
>>> print(json.og_dumps(some_dict))

Traceback (most recent call last):
TypeError: Object of type datetime is not JSON serializable
```

```python
>>> print(json.og_dumps(response))

Traceback (most recent call last):
TypeError: Object of type Response is not JSON serializable
```

I don't know why you'd want to put yourself through that pain, but if you do, it's there if you want it!  😉

If you want the power and convenience of giga_json's GigaEncoder serializer, but you want dumps to default to no line breaks and no indenting, use `flat_dumps()`:

```python
>>> print(json.flat_dumps(response))
{"fact": "Neutering a cat extends its life span by two or three years.", "length": 60}
```

## Behaviors
- when you do json.dumps(), you'll get pretty printed output by default (similar to pprint)
- objects like datetime that the standard json module will throw an Exception on will serialize correctly
- the other functions that come with the standard json module are included and are unmolested, so once you do: `import giga_json as json`, you can do json.load(), json.loads(), etc like you would with the standard module.
- the serializer has an intelligent order of checks.  for example, it checks for mapping before it tries iteration.  and before mapping, it checks the object for any built-in serialization methods, like to_json(), json(), etc.  this ensures that not only will your object be successfully serialized, but it will try the best method first
- if a serialization match and attempt fails, the serializer is allowed to continue down the list in the case that another method might match and work for the given object, increasing the chance of successful serialization
- .og_dumps() is an alias to the standard json.dumps() method, completely unchanged, if you need it
- .flat_dumps() uses giga_json's custom serializer, but its output argument defaults match standard json module, which means no pretty printing (no line breaks and no indents).  this is for convenience.  you can use normal dumps and pass in None for indent and False for sort_keys, and you will get an identical outcome
- being a simple function override, giga_json's dumps() function still allows you to pass in your own indent and sort_keys value, as well as using default= to pass in your own custom serializer

## What's actually different under the hood?

In reality, not much.  The biggest deviation from the standard json module is the custom serializer.  It's designed to handle almost anything you can throw at it.  I think the idea behind the standard module not handling things like datetime is out of need to draw the line somewhere, but also allowing users to choose HOW the data is serialized in specific cases, like how to format the timestamp in serialized form.  But having things like datetime handled by the module is not a bad thing in my opinion.  If the user wants a specific format, they should format it before they try to serialize their object.  I think we can only call it a downside if it permanently removes functionality you'd otherwise have.  But in the case of giga_json, you can still pass in your own indent and sort_keys values, and you can still use default= to pass in your own serializer, so you can use it the way you want.  You can even access the vanilla dumps() function via the alias og_dumps().  By defaulting to what most people expect and want most often, value is added.  If and when that default value isn't what they desire, they are free to handle it as they please, as this doesn't limit them from doing so. 

## More details about the differences?
- ### **vanilla json.dumps()**
  - defaults to `indent=None`, `sort_keys=False`
  - throws TypeError Exception if your data contains commonly used objects like datetime
- ### **giga_json's json.dumps()**
  - defaults to `indent=4`, `sort_keys=True`
  - uses custom GigaEncoder serializer that will serialize Python's most commonly used objects
  - 
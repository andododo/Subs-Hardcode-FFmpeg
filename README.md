# Subs Hardcode FFmpeg
I use this hand-in-hand with [anipy-cli](https://github.com/sdaqo/anipy-cli). Sometimes downloaded videos does not come with hardcoded subs, and just downloads a separate .vtt file. So I just merge them using this. 

Important to note: this is hardcoding the subs ONLY, I have a separate script for embedding the .vtt file (faster, like seconds). Check out [Subs-Embed](https://github.com/andododo/Subs-Embed).


## Quality Tweaks

You can expirement more by changing these values. Here are some examples which I find is the 'sweet-spot'.

Update: added sample presets .py files. 

### Faster (slightly lower quality)
```python
"-preset", "p6",
"-cq", "20",
```

### Higher quality (still fast)
```python
"-preset", "p4",
"-cq", "16",
```


## Managing output file

### Keep original MP4, output new file instead
change:
```python
temp_output = f"temp_{mp4}"
```

to:
```python
temp_output = f"burned_{mp4}"
```

and remove:
```python
safe_replace(...)
```


## Works with .mkv source
Updated the script to discover .mkv files as well.
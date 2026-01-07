# Some tweaks you can do

## Even faster (slightly lower quality)
"-preset", "p6",
"-cq", "20",

## Higher quality (still fast)
```python
"-preset", "p4",
"-cq", "16",
```

## Keep original MP4, output new file instead
Change:

```python
temp_output = f"temp_{mp4}"
```

to:

```python
temp_output = f"burned_{mp4}"
```

and `remove safe_replace(...)`.
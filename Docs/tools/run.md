# run

# Description

preset run script to run repetative tasks

## Usage
```
Usage: pt run [-h] [--file FILE] task

preset run script to run repetative tasks

positional arguments:
  task         The task to run

options:
  -h, --help   show this help message and exit
  --file FILE  The file to find the task in (default is {{cache}}/run.txt)
```

## documentation
### tasks
create one by adding the line `task <name>` to the file  
then add your steps below it  
close the task with `end`

### steps
steps are just commands that will be run in order
#### echo
`echo <message>`
prints a message to the console
#### run
`run <task>`
runs another task
#### cmd
`cmd <title> <command>`
opens a new terminal window with the given title and runs the command
#### browser
start with `browser new` 
then add `browser <url>` to add a new tab with the given url
add `browser open` to open all tabs
end with `browser close` to close the browser and clear the tabs list

## Slaying Ryu - Project for developing Django app for analysis and evaluation of time management system

App is fetching completed tasks from Google Tasks API and idea is to have nice
statistical presentation for analysis and evaluation of completed work.
Over time I have developed time managment system mainly inspired by Randy
Pausch. Idea is that TO-DO lists are organized by four categories:

* Important and Do Soon
* Important and Not Do Soon
* Not Important and Do Soon
* Not Important and Not Do Soon

Also every task has a tag which represents project or group of taks so
statistics can be easly filterd by it.

Project is using:
* south - for database migrations
* bootstrap3 - for UI
* djangobower - for easy install of bower apps jquery, d3.js etc.
* django nvd3 - for beautifull charts
* moment.js - for datetime library
* eonasdan-bootstrap-datetimepicker 

### Why Ryu?
**Ryu** is a Japanese dragon with three claws!!! And I'm gonna slay that
dragon! Haha. Essentially it's my attempt at going against my fear of
thinking that I can't be good programmer! Also this project is about time
management and learning Django so that's why I'm making Django app Kurama
that will slay dragon Ryu :-) 

### Current status
At the moment a lot of things are hard coded and badly written, I am aware of
that, but priority was to make any kind of working version.

### Setup instructions
Aside from virtualenv requirements.txt node.js and bower also need to be
installed. Then django's bower_install management command can be used to
installed required js libraries.

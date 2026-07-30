### EVENTIER EVENT MANAGEMENT PLATFROM

**Models.py details**

1. **CustomUser**
> User stored data's
> used to register users
-- 
2 . **Event**
> Registred user's can create,edit,delete and view events
> unregisterd user's can ony view events 
--
3 . **customfield**
> it allows user's to add extra question's of there kind
> it is connected to only one event so each event has their own questions to ask 
> other required models to complete it are chioce and customanswer
>*chioce*: this is to allow the user's to create options by them self's
> *customanswer*: this is give to the attendee to fill up 
--
4. **attendee**
> this is to represent user's and none user's that didn't that attended an event
> this allows but user's and none user's because by default it also collect info's that CustomUser have making it 
>> easy for none user's apply to an event


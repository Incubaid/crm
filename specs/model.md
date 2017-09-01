## phase 1

contact
- uid = random 4 letters/numbers e.g. sie7  (generated at start, check is unique)
- firstname
- lastname
- email addrs
- tel nrs
- message_channels = string: "E1,S2:T1"  e=email, s=sms, t=tel, b=bot, i=intercom  : means next level if first one failed
- description: markdown
- creationdate
- moddate
- owner (link to 1 contacs which is users)
- owner_backup (link to 1 contacs which is users)
- isuser : means can login using IYO
- telegram_bot: string (if user is on telegram & what is the botname used)

company
- uid = random 4 letters/numbers e.g. sie7  (generated at start, check is unique)
- name
- description: markdown
- email addrs
- tel nrs
- creationdate
- moddate
- owner (link to 1 contacs which is users)
- owner_backup (link to 1 contacs which is users)
- isuser : means can login using IYO

deal
- uid = random 4 letters/numbers e.g. sie7  (generated at start, check is unique)
- name
- contact_uid
- company_uid
- type: hoster, ito, pto, prepto
- state: new, interested, confirmed, waitingclose, closed
- remarks: markdown
- amount
- currency: USD/EUR/AED/GBP
- creationdate
- moddate
- closedate
- owner (link to 1 contacs which is users)
- owner_backup (link to 1 contact which is users)

comment
- uid = random 4 letters/numbers e.g. sie7  (generated at start, check is unique)
- contact_uid
- deal_uid
- project_uid
- organization_uid
- task_uid
- sprint_uid
- creationdate
- moddate
- content (is markdown)
- owner (link to 1 contact which is users)

link
- uid
- url
- descr (markdown optional)
- labels = text e.g. '''color:green level:important'''
- comment_uid
- contact_uid
- deal_uid
- project_uid
- organization_uid
- task_uid

task
- uid
- title
- type: feature, question, task, story, contact
- description (markdown)
- urgency: critical, urgent, normal, minor
- deal_uid
- project_uid
- organization_uid
- sprint_uid : link to in which sprint this needs to be done
- owner (link to 1 contact which is users)
- percent completed (calculated from task_assignments)
- time_todo
- time_done

task_assignment
- uid
- contact_uid
- task_uid
- time_todo (h)
- percent_completed

task_tracking
- uid
- task_assignment_uid
- remark: markdown
- time_done (h) (can be 0.5)
- epoch (can be overruled, if empty current time)

organization
- uid = random 4 letters/numbers e.g. sie7  (generated at start, check is unique)
- name
- description: markdown
- creationdate
- moddate
- promotor (link to 1 contacs which is users)
- guardian (link to 1 contacs which is users)
- parent_uid (link to potential parent)

organization_user
- contact_uid
- organization_uid

project
- uid = random 4 letters/numbers e.g. sie7  (generated at start, check is unique)
- name
- description: markdown
- creationdate
- moddate
- startdate
- deadline
- perc_done
- promotor (link to 1 contacs which is users)
- guardian (link to 1 contacs which is users)
- parent_uid (link to potential parent)


project_user
- contact_uid
- project_uid

sprint
- uid
- name
- description (markdown)
#sprint can be defined for project & organization, even together
- project_uid
- organization_uid
- startdate
- deadline
- creationdate (auto)
- moddate (auto)
- percentdone (is calculated)
- hoursopen (is calculated)
- hoursopen_person_avg (is calculated)
- hoursopen_person_max (is calculated)
- owner (link to 1 contact which is user)


message
- uid
- title
- content (markdown)
- tosend_time : epoch when to send
- send_time: time it was send
#message can be for a contact, deal, ... even linked to more than 1
- array: contact_uid
- organization_uid
- deal_uid
- project_uid
- task_uid
- sprint_uid
- channel: telegram, email, sms, intercom
- require_confirmation: bool  (will send e.g. link in email which will confirm reception)

## phase 2

source
- uid
- title
- description
- url

alert
- uid
- title
- content (markdown)
- starttime
- state: new, confirmed, closed
- urgency: critical, urgent, normal, minor
- data (for e.g. toml, json or yaml structure content)
- alert_profile
#can be linked to multiple pieces of info
- organization_uid
- deal_uid
- project_uid
- task_uid
- source_uid
- source_id #whatever id used on source
#can be more than 1 at same time
- type_down: bool (if there is downtime)
- type_performance: bool
- type_security: book
- type_instability: bool
- type_ui :userinterface

alert_profile
- uid
- name
- description (markdown)
- configuration: is toml config, depends on type of profile, what this configuration is

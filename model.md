

contact
- uid = random 4 letters/numbers e.g. sie7  (generated at start, check is unique)
- firstname
- lastname
- email addrs
- tel nrs
- description
- creationdate
- moddate
- owner (link to 1 contacs which is users)
- owner_backup (link to 1 contacs which is users)
- isuser : means can login using IYO

company
- uid = random 4 letters/numbers e.g. sie7  (generated at start, check is unique)
- name
- description
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
- remarks
- amount
- currency: USD/EUR/AED/GBP
- creationdate
- moddate
- closedate
- comments
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
- remark (is markdown)
- owner (link to 1 contact which is users)

task
- uid
- title
- type: feature, question, task, story, contact
- description (markdown)
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
- remark
- time_done (h) (can be 0.5)
- epoch (can be overruled, if empty current time)

organization
- uid = random 4 letters/numbers e.g. sie7  (generated at start, check is unique)
- name
- description
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
- description
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



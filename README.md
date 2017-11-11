# Catalog
Udacity - Full Stack - Project 4

## 1 Description

This application provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

### Database

Table 1 - user 

|  id (primary key)  |  name  |  email  |
|  :--:  |  :--:  |  :--:  |

Table 2 - category

|  name (primary key)  |
|  :--:  |

Table 3 - category_item

|  name (primary key)  |  description  |  category.name  |  user.id  |
|  :--:  |  :--:  |  :--:  |  :--:  |


### Endpoints

`localhost:8000/` : index page, show all categories and 10 recently added items, you can add item after login.

`/catalog/<string:category_name>/items` : show all the items belong to category_name.

`/catalog/<string:category_name>/<string:item_name>` : show the description of item_name, if you were the creater of this item, you can also edit or delete it.

`/add` : Add a new item after login.

`/catalog/<string:item_name>/edit` : Edit the item you created.

`/catalog/<string:item_name>/delete` : Delete the item you created.

`/catalog.json` : show all items in JSON format.




## 2 Install Vagrant and VirtualBox

### Vagrant

Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. You can download it from <a href="https://www.vagrantup.com/" target="_blank">vagrantup.com</a>. Install the version for your operating system.

### VirtualBox

VirtualBox is the software that actually runs the VM. You can download it from <a href="https://www.virtualbox.org/" target="_blank">virtualbox.org</a>. Install the platform package for your operating system. You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it.


## 3 Run this project

Clone this repo:

`$ git clone https://github.com/TianyangChen/Catalog.git`

Change directory:

`$ cd Catalog/vagrant`

Run the virtual machine:

```
$ vagrant up
$ cd /vagrant/catalog
```

Initialize the database and add some items:

```
$ python database_setup.py
$ python add_data.py
```

Run this project:

`python application.py`

Open your favorite web browser, visit: 

`http://localhost:8000`


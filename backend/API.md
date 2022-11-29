# API

以下均省略``localhost:xxxx/``

## USER

* ``user/login/``

  ``POST``

  ```python
  I: 
      {
          "username": xxx,
          "password": xxx
      }
  
  O:
      # success
      {
          "code": x,
          "id": xx,
          "username": xx,
          "email": xx,
          "avatar": xx,
          "date_joined": xx,
          "question": xx,
          "answer": xx,
          "last_name": xx,
          "first_name": xx,
          "age": xx,
          "country": xx,
          "tot_like": xx,
          "tot_dislike": xx
      }
      
      # fail
      {
          "code": x
      } 
      
  # code:
  # 0 --> success
  # 1 --> username or password is wrong
  # 2 --> request method is not POST
  # 3 --> user who has entered can't log in again
  ```

* ``user/signup/``

  ``POST``

  ```python
  I: 
      {
          "username": xxx,
          "password": xxx
      }
  
  O:
      {
          "code": x
      } 
          
  # code:
  # 0 --> success
  # 1 --> username has already existed
  # 2 --> request method is not POST
  # 3 --> user who has logged in cannot sign up
  ```

* ``user/logout/``

  ``GET``

  ```python
  O:
      {
          "code": x
      }
      
  # code:
  # 0 --> success
  # 1 --> user who has not logged in cannot log out
  ```

  

* ``user/follow/``

  ``POST``

  ```python
  O:
      {
          "code": x
      }
      
  # code:
  # 0 --> success 
  # 1 --> cancel follow
  # 2 --> request method is not POST
  # 3 --> visitor needs to log in
  # 4 --> user cannot follow himself
  
  # if you have followed sb, you will unfollow him
  # after you click the button again
  ```

* ``user/fixProfile/``

  ``POST``

  前端检测：

  * ``avatar``为图片
  * ``question``与``answer``必须同时为空或不为空，
  * **其它格式检验**

  如果有修改就传值否则值为空

  ```python
  I:
      {
          "username": xx,
          "password": xx,
          "email": xx,
          "file": xx, # avatar
          "question": xx,
          "answer": xx,
          "lastname": xx,
          "firstname": xx,
          "age": xx,
          "country": xx
      }
  
  O:
      {
          "code": xx
      }
  
  # code:
  # 0 --> success 
  # 1 --> username has been used by others or username doesn't change
  # 2 --> request method is not POST
  # 3 --> user should sign in before
  # 4 --> avatar upload error
  ```
  
  只有``code``为$0$，数据库发生修改

* ``user/getProfile``

  ``POST``
  
  ```python
  I:
        {
            "username": xx
        }
    
  O:
        # success
        # 0, 1
        {
            "code": x,
            "id": xx,
            "username": xx,
            "email": xx,
            "avatar": xx,
            "date_joined": xx，
            "question": xx,
            "answer": xx,
            "last_name": xx,
            "first_name": xx,
            "age": xx,
            "country": xx,
            "tot_like": xx,
            "tot_dislike": xx
        }
        
        # fail
        # 1
        {
            "code": x
        } 
    
    # code:
    # 0 --> success
    # 1 --> username is "" or username is not the user who is enquirying
  ```

* ``user/getContacts/``

  ``GET``

  返回和当前登陆用户互关的所有人

  ```python
      
  O:
      [
          {
              "username": xxx,
              "avatar": xxx
          }
          {
              "username": xxx,
              "avatar": xxx
          }
          ...
      ]
  ```

## SHOP

* ``shop/fetchAll/``

  ``GET``

  ```python
  O:  
      [
          {
              "id": xx,
              "name": xx,
              "image": xx,
              "price": xx,
              "time": xx,
              "username": xx,
              "tot_like": xx,
              "tot_dislike": xx,
              "tot_comment": xx
          }
          {
              ...
          }
          ...
       ]
  ```

  找不到全为空

* ``blog/fetchUserMerchandises/``

  ``POST``

  前端检查登陆

  ```python
  I:
      {
          "username": xx,
          # sort
          "op": xx, # 0: newest, 1: rank:Hight-Low, 2: price:Hight-Low, 3: price:Low-High
          # filters
          "sale": xx, # bool
          "new": xx, # bool
          "category": xx, # "" for all
          "color": xx, # "" for all
          "priceSale": xx, # 0: priceSale<=25, 1: 25<priceSale<=75, 2: priceSale>75, 3: all
          "rank": xx, # rank>=xx
      }
  
  O:  
      [
          {
              "id": xx,
              "name": xx,
              "description": xx,
              "image": xx,
              "deliveryLocation": xx,
              "deliveryTime": xx,
              "price": xx,
              "time": xx,
              "username": xx,
              "tot_like": xx,
              "tot_dislike": xx,
              "rank": xx, # 0~5 caculate from tot_like and tot_dislike
              "color": [xx, xx, ...] 
              # choose from ['#00AB55', '#000000', '#FFFFFF', '#FFC0CB', 
              				'#FF4842', '#1890FF', '#94D82D', '#FFC107']
              				
              "priceSale": xx, 
              "status": xx, # 0: normal, 1: sale, 2: new
              "category": xx, # choose from ['food', 'clothing', 'book', 'decoration', 'digital', 'other']
          }
          {
              ...
          }
          ...
       ]
  ```

* ``shop/postMerchandise/``

  `POST`

  ```python
  I:
      {
         "image": xx,
         "name": xx, 
         "description": xx,
         "price": xx,
         "priceSale": xx,
         "deliveryLocation": xx,
         "deliveryTime": xx,
         "category": xx,
         "color": [xxx, xx],
      }
  
  O:  
  ```

* ``shop/getMerchandise/``

  ``POST``

  ```python
  I:
      {
          "id": xx
  	}
      
  O:
      {
           	"id": xx,
              "name": xx,
              "description": xx,
              "image": xx,
              "deliveryLocation": xx,
              "deliveryTime": xx,
              "price": xx,
              "time": xx,
              "username": xx,
              "tot_like": xx,
              "tot_dislike": xx,
              "rank": xx, # 0~5 caculate from tot_like and tot_dislike
              "color": [xx, xx, ...] 
              # choose from ['#00AB55', '#000000', '#FFFFFF', '#FFC0CB', '#FF4842', '#1890FF', '#94D82D', '#FFC107']
              				
              "priceSale": xx, 
              "status": xx, # 0: normal, 1: sale, 2: new
              "category": xx, # choose from ['food', 'clothing', 'book', 'decoration', 'digital', 'other']
      }
  ```
  

* `shop/delMerchandise/`

  `POST`

  ```python
  I:
      {
          id:xx
      }
  
  # 403 --> fobid
  # 401 --> log in before
  # 404 --> not found
  ```


* ``shop/fixMerchandise/``

  ``POST``

  ```python
  I:
      {
         id: xx,
         image: xx,
         name: '', 
         description: '',
         price: '',
         priceSale: '',
         deliveryLocation: '',
         deliveryTime: '',
         category: '',
         color: xx,xxx,
      }
      
  # 403 --> fobid
  # 401 --> log in before
  # 404 --> not found
  ```

  

## BLOG

* ``blog/fetchAll/``

  ``GET``

  * ``tag``用逗号分隔
  * ``follow``字符串，``true``或``""``

  逻辑：

  * ``follow``：为``true``，如果用户未登陆返回空，否则搜索用户以及与他关联的用户文章
  * ``tag``：需要全满足才返回
  * ``search``：编辑距离匹配``title``，``ratio``达到$30\%$即可

  以上过程可以叠加，如果有字段为空表示不需要按照该字段筛选，同时如果某字段的筛选为空会直接返回空

  ```python
  I:
      {
          "follow": xx,
          "tag": xx,
          "search": xx
      }
  
  O: 
      [
          {
              "authorName": xx,
              "releaseTime": xx,
              "categories": [xx, yy ...], # maybe is an empty list
              "title": xx,
              "digest": xx,
              "userPhoto": xx,
              "cover": xx,
              "html": xx,
              "id": xx,
              "tot_like": xx,
              "tot_dislike": xx,
              "tot_comment": xx,
              "followed": xx
          }
          {
              ...
          }
          ...
      ]
  ```

  找不到全为空

* ``blog/fetchOne/``

  ``POST``

  ```python
  I:
      {
          "author_Name": xxx,
          "tit": xxx
      }
      
  O:
  	{
         "authorName": xx,
          "releaseTime": xx,
          "categories": [xx, yy ...], # maybe is an empty list
          "title": xx,
          "digest": xx,
          "userPhoto": xx,
          "cover": xx,
          "html": xx,
          "id": xx,
          "tot_like": xx,
          "tot_dislike": xx,
          "tot_comment": xx
      }
  ```

  找不到全为空

* ``blog/delete/``

  ``POST``

  ```python
  I:
      {
          "username": xxx,
          "tit": xxx
      }
  
  O:
      {
          "code": xx
      }
  
  # code:
  # 0 --> success
  # 1 --> article doesn't exist
  # 2 --> request method is not POST
  # 3 --> the user is not the author of the article or the user is not admin or the user has not logged in
  ```


* ``blog/uploadPicture/``

  ``POST``

  ```python
  I:
      {
          "picture": xxx
  	}
      
  O:
      {
          "code": xxx,
          "url": xxx
  	}
      
  # code:
  # 0 --> success
  # 1 --> error, the value of url is ""
  ```

* ``blog/postArticle/``

  ``POST``

  ```python
  I:
      {
          "html": xxx,
          "tags": xxx,
          "title": xxx,
          "cover": xxx
      }
      
  O:
      {
      	"code": xxx 
  	}
      
  # code:
  # 0 --> success
  # 1 --> please sign in before
  # 2 --> the user had posted an article whose name is the same as the one being posted now
  ```

  ``tags``：xxx,xxx,xxx,xxx

* ``blog/fetchUserArticles/``

  ``POST``

  前端检查登陆

  ```python
  I:
        {
            "op": xx, # 0: descend, 1: ascend 
            "username": xx
        }
        
    O:
    	[
            {
               "authorName": xx,
                "releaseTime": xx,
                "categories": [xx, yy ...], # maybe is an empty list
                "title": xx,
                "digest": xx,
                "userPhoto": xx,
                "cover": xx,
                "html": xx,
                "id": xx,
                "tot_like": xx,
                "tot_dislike": xx,
                "tot_comment": xx
        	}
            {
                ...
            }
            ...
        ]
  ```
  
* ``blog/uploadVideo/``

  ``POST``

  ```python
  I:
      {
          "video": xxx
  	}
      
  O:
      {
          "code": xxx,
          "url": xxx
  	}
      
  # code:
  # 0 --> success
  # 1 --> error, the value of url is ""
  ```

## MOMENT

* ``moment/sendMoment/``

  ``POST``

  如果``content``为空返回所有，否则返回当前更新后的所有
  
  ```python
  I:
      {
          "content": xxx
      }
  
  O:
      # sucess
      {
          "code": xx
          "data": [
              {
                  "username": xxx,
                  "avatar": xxx,
                  "content": xxx,
                  "time": xxx,
                  "id": xx,
                  "tot_like": xx,
                  "tot_dislike": xx,
                  "tot_comment": xx,
                  "stance": xx
              }
              {
                  ....
              }
              ...
          ]  
      }
      
      # fail
      {
          "code": xx
      }
      
  # code:
  # 0 --> success
  # 1 --> please sign in before
  ```

* ``moment/getMoment/``

  ``POST``

  返回对应id的moment
  
  ```python
  I:
      {
          "id": xxx
      }
  
  O:
    # sucess
      {
          "username": xxx,
          "avatar": xxx,
          "content": xxx,
          "time": xxx,
          "id": xx,
          "tot_like": xx,
          "tot_dislike": xx,
          "tot_comment": xx,
          "stance": xx
      }
  ```

* ``moment/delMoment/``

  ``POST``

  删除对应id的moment，如果不是管理员/创作者则无法删除

  ```python
  I:
      {
          "id": xxx
      }
  
  # 401 --> login before
  # 403 --> not the author
  # 200 --> ok
  ```

## CHAT

**注意避免游客访问，后端就不检查了**

* ``chat/getChats/``

  ``GET``

  **注意存``id``！！！！**
  
  如果``name``是空的话就返回所有和当前登陆用户聊过天的对话；
  
    反之进行模糊匹配，返回所有差不多的对话；
  

  ```python
  I:
      {
          "name": xxx
      }
  O:
      [
          {
              "id": xxx, # private chat(group chat) id
              "type": xxx, # private chat(group chat)
              "name": xxx, # "" if the chat is a private chat 
              "time": xxx, # creating time
              "owner": xxx, # sponsor
              "avatar": xxx,
              "latest": { # maybe is {}
                  "username": xxx,
                  "content": xxx,
                  "avatar": xxx,
                  "time": xxx
              }
          }
          {
              ...
          }
          ...
      ]
  ```

* ``chat/createChat/``
    注意``name``为空**当且仅当**是私聊，此时``username``必须为``xx,xx``格式，不能
    有多余逗号或者空格，同时必须刚好两个人，``name``不为空则为群聊

  ``POST``

  ```python
   I:
      {
          "username": xxx,yyy,zzz,
          "name":xxx #group name #"" if the chat is a private chat 
      }
      
  O:
      {
              "id": xxx, # private chat(group chat) id
              "type": xxx, # private chat(group chat)
              "name": xxx, # "" if the chat is a private chat 
              "time": xxx, # creating time
              "owner": xxx, # sponsor
              "avatar": xxx,
          	"latest": { # maybe is {}
                  "username": xxx,
                    "content": xxx,
                    "avatar": xxx,
                    "time": xxx
                }
        }
  ```
  
* ``group/getRecords/``

  ``GET``

  ```python
  I:
      {
          "id": xxx # group(private or group) id
      }
      
  O:
      [
          {
              "sender": xxx, # the user loging in now: 0, other: 1
              "username": xxx,
              "avatar": xxx,
              "content": xxx,
              "time": xxx
          }
          {
              ...
          }
          ...
      ]
  ```

* ``chat/sendRecord/``

  ``POST``

  ```python
  I:
      {
          "id": xxx, # group(private or group) id
          "content": xxx,
      }
      
  O:
      [
          {
              "sender": xxx, # the user loging in now: 0, other: 1
              "username": xxx,
              "avatar": xxx,
              "content": xxx,
              "time": xxx,
          }
          {
              ...
          }
          ...
      ]
  ```
  
* ``group/addContact/``

  ``POST``

  把一些人加入群聊

  ```python
   I:
      {
          "username": xxx,yyy,zzz
          "id":xxx #group chat id 
      }
  
  O:
      {
            "id": xxx, # private chat(group chat) id
            "type": xxx, # private chat(group chat)
            "name": xxx, # "" if the chat is a private chat 
            "time": xxx, # creating time
            "owner": xxx, # sponsor
            "avatar": xxx,
            "latest": { # maybe is {}
                "username": xxx,
                  "content": xxx,
                  "avatar": xxx,
                  "time": xxx
              }
      }
  ```



## RESPONSE

**前端检查登陆**

* ``response/takeStance/``

  ``POST``

  ```python
  I:
      {
          "obj_type": xx, # 0, 1, 2, 3, 4
          "obj_id": xx
          "stance": 1/0/-1
      }
      
  O:
      {
          "tot_like": xxx,
          "tot_dislike": xxx
      }
      
  # ---------------------------------
  #		(obj_type, obj)
  #     ====================
  #		(0, 'moment'),
  #		(1, 'article'),
  #		(2, 'comment'),
  #		(3, 'merchandise'),
  #		(4, 'user'),
  #  ----------------------------------
  # 		(stance_id, stance)
  #	=============================
  # 		(0, 'neutral')
  #		(1, 'support')
  #		(-1, 'oppo')
  ```

  

* ``response/addComment/``

  ``POST``

  ```python
  I:
      {
          "obj_type": xx, # 0, 1, 2, 3, 4
          "obj_id": xx,
          "content": xx
      }
      
      
  O:
      {
          "id": xx
      }
      
  # ---------------------------------
  #		(obj_type, obj)
  #     ====================
  #		(0, 'moment'),
  #		(1, 'article'),
  #		(2, 'merchandise'),
  ```
  
* ``response/delComment/``

  ``POST``

  ```python
  I:
      {
          "id": xx
      }
      
  # 401 --> login before
  # 403 --> not the author
  # 200 --> ok
  ```
  
* ``response/findComment/``

  ``POST``

  ```python
  I:
      {
          "id": xx
      }
      
  O:
      {
          "username": xx,
          "avatar": xx,
          "time": xx,
          "content": xx,
          "tot_like": xx,
          "tot_dislike": xx,
          "id": xx
      }
  ```


* ``response/findComments/``

  ``POST``

  ```python
  I:
      {
          "obj_type": xx, # 0, 1, 2, 3, 4
          "obj_id": xx,
      }
      
  O:
      [
          {
              "username": xx,
              "avatar": xx,
              "time": xx,
              "content": xx,
              "tot_like": xx,
              "tot_dislike": xx,
              "stance": xx,
          	"id": xx
      	}
          {
              ...
          }
          ...
      ]
      
  # ---------------------------------
  #		(obj_type, obj)
  #     ====================
  #		(0, 'moment'),
  #		(1, 'article'),
  #		(2, 'merchandise'),
  ```

  


------

## log:

* 2022/11/12/23:30: 添加完成``postArticle``、``uploadPicture``、``getProfile``、修改``fetchAll``、对于所有``fetch*``当为空时改为返回会``{}``或者``[]``，并完成简单测试

* 2022/11/13/17:00：对于``blog``而言调整``fetchOne``格式与``fetchAll``格式一致，完成``sendMoment``，大改完成``fetchAll``（``blog``）

* 2022/11/13/23:00：调整``sendMoment``

* 2022/11/14/21:00:	完成``getChats``、``findUser``、``getRecords``、``sendRecord``

* 2022/11/15/18:00: 加入``comment``、``like``、``dislike``，修改``profile``相关接口

* 2022/11/15/23:00: 修改所有接口加入``id``、``tot_dislike``、``tot_like``、``tot_comment``，对于每条``record``任然没有传``id``，新增``fetchUserArticles``和``fetchUserMerchandises``，明天继续完善``response``，暂时只有数据库没有可用``api``，修改``getProfile``

* 2022/11/16/20:30: 修改`getChats`，新增`createChat`，删除``findUser``，完成``takeStance``

* 2022/11/19/22:00: 改``fetchUserMerchandises``，新增``getMerchandise``、``postMerchandise``

* 2022/11/20/19:00: 完成``addComment``、``delComment``、``findComment``、``findComments``，在``blog``的``fetchAll``加入``followed``字段，``findComents``、``sendMoment``加入``stance``字段

* 2022/11/22/20:00：新增``user/getContacts/``、``chat/addMember/``、``moment/getMoment/``、``moment/delMoment/``，注意看``createChat``的``I``和``O``

* 2022/11/23/00:30，新增``fixMerchandise``、``delMerchandise``

  
  
  
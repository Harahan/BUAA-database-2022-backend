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
          "date_joined": xx
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
          "avatar": xx,
          "question": xx,
          "answer": xx
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

  ``GET``

  ```python
  O:
      # success
      {
          "code": x,
          "id": xx,
          "username": xx,
          "email": xx,
          "avatar": xx,
          "date_joined": xx
      }
      
      # fail
      {
          "code": x
      } 
  
  # code:
  # 0 --> success
  # 1 --> you should sign in before
  ```

## SHOP

* ``shop/fetchAll/``

  ``GET``

  ```python
  O:  
      {
          {
              "name": xx,
              "image": xx,
              "price": xx
          }
          {
              ...
          }
          ...
      }
  ```

  如果为空或者不是``GET``，返回``404``

## BLOG

* ``blog/fetchAll/``

  ``GET``

  ```python
  O: 
      {
          {
              "authorName": xx,
              "releaseTime": xx,
              "categories": [xx, yy ...], # maybe is an empty list
              "title": xx,
              "digest": xx,
              "userPhoto": xx,
              "cover": xx,
              "html": xx
          }
          {
              ...
          }
          ...
      }
  ```

* ``blog/fetchOne/``

  ``GET``

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
          "categories": xx,
          "title": xx,
          "digest": xx
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

------

## log:

* 2022/11/12/23:30: 添加完成``postArticle``、``uploadPicture``、``getProfile``、修改``fetchAll``、对于所有``fetch*``当为空时改为返回会``{}``，并完成简单测试


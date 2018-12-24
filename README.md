# ZhihuUser

爬取知乎用户信息十万条（仅做技术学习，不可用于商业行为）

简述：
知乎网站是大型问答类网站，本爬虫通过json接口爬取知乎注册用户的相关信息，包括用户的昵称、id、关注数、文章数、回答数等。本爬虫反爬使用蜻蜓ip代理，通过api每十秒获取十个代理ip，与免费的代理ip相比，可用率高，延迟低，大大增加了爬取的速度。

结果：
数据十万零一条，用时38分钟

接口：
https://www.zhihu.com/api/v4/members/su-fei-17/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20

截图（加载较慢）
![image](https://github.com/LemonBottom/ZhihuUser/blob/master/images/zhihuUser1.png?raw=true)
![image](https://github.com/LemonBottom/ZhihuUser/blob/master/images/zhihuUser2.jpg?raw=true)
![image](https://github.com/LemonBottom/ZhihuUser/blob/master/images/zhihuUser3.png?raw=true)

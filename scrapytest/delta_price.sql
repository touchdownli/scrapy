select c.id, d.list_price as last_price,e.list_price as price,(e.list_price-d.list_price) as delta,f.* from
	(select a.id,a.min,b.max from
		(select id,min(crawl_date) as min from second_hand_house_price_info group by id having count(*)>1) as a
		inner join
		(select id,max(crawl_date) as max from second_hand_house_price_info group by id) as b
		on a.id=b.id
	) c
inner join
	second_hand_house_price_info as d
on c.id=d.id and c.min=d.crawl_date
inner join
	second_hand_house_price_info as e
on c.id=e.id and c.max=e.crawl_date
inner join
	lianjia_house as f
on c.id=f.id
order by delta;
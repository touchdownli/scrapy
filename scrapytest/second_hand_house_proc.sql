delimiter //
CREATE procedure PROC_second_hand_house_select(
	in cityName nvarchar(10)
	)
begin
	SELECT
    `c`.`id` as 'cid',
	  `d`.`list_price` AS 'last_price',
	  `e`.`list_price` AS 'price',
	  (`e`.`list_price` - `d`.`list_price`) AS 'delta',
	  `f`.*
	FROM
	  (SELECT
	    `a`.`id`, `a`.`min`, `b`.`max`
	  FROM
	    (SELECT
	      `id`, MIN(`crawl_date`) AS 'min'
	    FROM
	      `second_hand_house_price_info`
	    GROUP BY
	      `id`
	    HAVING
	      COUNT(*) > 1) AS a
	      INNER JOIN (SELECT
	        `id`, MAX(`crawl_date`) AS 'max'
	      FROM
	        `second_hand_house_price_info`
	      GROUP BY
	        `id`) AS b ON `a`.`id` = `b`.`id`) c
	    INNER JOIN `second_hand_house_price_info` AS d ON `c`.`id` = `d`.`id` AND `c`.`min` = `d`.`crawl_date`
	    INNER JOIN `second_hand_house_price_info` AS e ON `c`.`id` = `e`.`id` AND `c`.`max` = `e`.`crawl_date`
	    INNER JOIN (select * from `lianjia_house` where city=cityName) AS f ON `c`.`id` = `f`.`id`
	WHERE
	  (`e`.`list_price` - `d`.`list_price`) <0
	ORDER BY `delta`;
end //
delimiter ;
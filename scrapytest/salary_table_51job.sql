CREATE TABLE `salary` (
  SELECT
    `ID`, IF(`salary_range` LIKE '%万/月', SUBSTRING_INDEX(`salary_range`, '-', 1) * 10000, IF(`salary_range` LIKE '%万/年', ROUND(SUBSTRING_INDEX(`salary_range`, '-', 1) * 10000 / 12, 0), IF(`salary_range` LIKE '%千/月', SUBSTRING_INDEX(`salary_range`, '-', 1) * 1000, 0))) AS 'salary_min', IF(`salary_range` LIKE '%万/月', SUBSTRING_INDEX(`salary_range`, '-', -1) * 10000, IF(`salary_range` LIKE '%万/年', ROUND(SUBSTRING_INDEX(`salary_range`, '-', -1) * 10000 / 12, 0), IF(`salary_range` LIKE '%千/月', SUBSTRING_INDEX(`salary_range`, '-', -1) * 1000, 0))) AS 'salary_max', SUBSTRING_INDEX(`location_name`, '-', -1) AS 'location_name'
  FROM
    `job`
)
# !/usr/bin/python
# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from handling_salary_time import *
from scrapy import Selector
import uuid
import re
import time


# 解析简历函数
def handle_juxian(d={}):
	"""
	解析猎聘简历的方法，最后返回解析好的dict 类型resume
	:param d:
	:return:
	"""
	resume = {"resume_id": "", "cv_id": "", "phone": "", "name": "", "email": "", "create_time": long(0),
			  "crawled_time": long(0), "update_time": "", "resume_keyword": "", "resume_img": "",
			  "self_introduction": "", "expect_city": "", "expect_industry": "", "expect_salary": "",
			  "expect_position": "", "expect_job_type": "", "expect_occupation": "", "starting_date": "", "gender": "",
			  "age": "", "degree": "", "enterprise_type": "", "work_status": "", "source": "", "college_name": "",
			  "profession_name": "", "last_enterprise_name": "", "last_position_name": "",
			  "last_enterprise_industry": "", "last_enterprise_time": "", "last_enterprise_salary": "",
			  "last_year_salary": "", "hometown": "", "living": "", "birthday": "", "marital_status": "",
			  "politics": "", "work_year": "", "height": "", "interests": "", "career_goal": "", "specialty": "",
			  "special_skills": "", "drive_name": "", "country": "", "osExperience": "", "status": "0", "flag": "0",
			  "dimension_flag": False, "version": [], "keyword_id": [], "resumeUpdateTimeList": [], "educationList": [],
			  "workExperienceList": [], "projectList": [], "trainList": [], "certificateList": [], "languageList": [],
			  "skillList": [], "awardList": [], "socialList": [], "schoolPositionList": [], "productList": [],
			  "scholarshipList": []}

	"""
	简历resume 对象属性的默认值
	设置默认值的作用是保证与数据库中其他数据类型的数据格式进行统一化
	"""
	# 来源
	resume["source"] = u"举贤网"
	# 状态
	resume["status"] = "0"
	# 标志
	resume["flag"] = "0"
	# dimension_flag
	resume["dimension_flag"] = False
	# 简历ID
	resume["resume_id"] = str(uuid.uuid4()).replace("-", "")

	# resume["cv_id"]
	resume["cv_id"] = "juxian" + resume["resume_id"]

	# 更新时间
	resume["update_time"] = "2014-12-31"
	# 爬取时间
	resume["crawled_time"] = long(1420002000000)
	# create_time
	resume["create_time"] = long(time.time() * 1000)

	if "content" in d and len(d["content"]) > 0:
		re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
		# re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)
		re_comment = re.compile('<!--[^>]*-->')  # HTML注释
		re_script = re.compile(r'<script[^>]*?>[\s\S]*?<\/script>', re.I)
		s = d["content"]
		s = re_style.sub("", s)
		s = re_script.sub("", s)
		s = re_comment.sub("", s)

		s = s.replace(r'\"', '')
		main_info = Selector(text=d["content"]).xpath("body//div[@class='gongyongw']")
		if len(main_info) > 0:
			handle_html(resume, main_info[0])
		else:
			resume = {}

	# print resume
	# 返回解析好的简历 resume
	return resume


def handle_html(resume, main_info):
	# print main_info.extract()
	div_infos = main_info.xpath(".//div[@class='title_h3v6']")
	if len(div_infos) > 0:
		for i in range(len(div_infos)):
			info = div_infos[i].xpath("following-sibling::table[1]")
			div_temp = div_infos[i].xpath("string(.)")
			if len(div_temp) > 0:
				div_text = div_temp[0].extract().strip()
				if u"个人信息" in div_text:
					if len(info) > 0:
						# 处理个人信息
						handle_person_info(resume, info[0])
						continue
				elif u"求职意向" in div_text:
					if len(info) > 0:
						# 处理求职意向
						handle_career_info(resume, info[0])
						continue
				elif u"目前年薪" in div_text:
					if len(info) > 0:
						# 处理目前年薪
						handle_last_salary(resume, info[0])
						continue
				elif u"自我评价" in div_text:
					if len(info) > 0:
						# 处理自我评价
						handle_self_intro(resume, info[0])
						continue
				elif u"工作经历" in div_text:
					if len(info) > 0:
						# 处理工作经历
						work_div = div_infos[i].xpath("following-sibling::div[@class='gongzuojl']")
						handle_work_exp(resume, work_div)
						continue
				elif u"教育经历" in div_text:
					if len(info) > 0:
						# 处理教育经历
						handle_edu_exp(resume, info[0])
						continue
				elif u"项目经验" in div_text:
					if len(info) > 0:
						work_div = div_infos[i].xpath("following-sibling::div[@class='gongzuojl']")
						# 处理项目经验
						handle_proj_exp(resume, work_div)
						continue
				elif u"语言能力" in div_text:
					if len(info) > 0:
						# 处理语言能力
						handle_language(resume, info[0])
						continue
				elif u"所获证书" in div_text:
					if len(info) > 0:
						# 处理证书信息
						cert_div = div_infos[i].xpath("following-sibling::div[@class='gongzuojl']")
						handle_certification(resume, cert_div)
						continue

	# 添加最后一份工作信息
	for i in range(len(resume["workExperienceList"])):
		if resume["last_enterprise_name"] == "":
			resume["last_enterprise_name"] = resume["workExperienceList"][i].get("enterprise_name")
		if resume["last_enterprise_industry"] == "":
			resume["last_enterprise_industry"] = resume["workExperienceList"][i].get("enterprise_industry")
		if resume["last_enterprise_time"] == "":
			resume["last_enterprise_time"] = resume["workExperienceList"][i].get("work_time")
		if resume["last_enterprise_salary"] == "":
			resume["last_enterprise_salary"] = resume["workExperienceList"][i].get("salary")
		if resume["last_position_name"] == "":
			resume["last_position_name"] = resume["workExperienceList"][i].get("position_name")

	# 添加学历信息
	for i in range(len(resume["educationList"])):
		if resume["degree"] == "":
			resume["degree"] = resume["educationList"][i].get("degree")
		if resume["college_name"] == "":
			resume["college_name"] = resume["educationList"][i].get("college_name")
		if resume["profession_name"] == "":
			resume["profession_name"] = resume["educationList"][i].get("profession_name")

	# 返回解析好的简历resume
	return resume


def handle_person_info(resume, info):
	td_infos = info.xpath(".//td[@class='telr']")
	if len(td_infos) > 0:
		for i in range(len(td_infos)):
			td_temp = td_infos[i].xpath("following-sibling::td[1]/text()")
			if len(td_temp) > 0:
				# print td_infos[i].extract()
				if u"姓名" in td_infos[i].extract():
					resume["name"] = td_temp[0].extract().strip()
					continue
				elif u"性别" in td_infos[i].extract():
					resume["gender"] = td_temp[0].extract().strip()
					continue
				elif u"电子邮件" in td_infos[i].extract():
					resume["email"] = td_temp[0].extract().strip()
					continue
				elif u"出生年月" in td_infos[i].extract():
					birth = td_temp[0].extract().strip()
					if re.match(u"(\d{4})年(\d{2})月", birth):
						resume["birthday"] = re.match(u"(\d{4})年(\d{2})月", birth).group(1) + "-" + re.match(
							u"(\d{4})年(\d{2})月", birth).group(2)
					continue
				elif u"手机号码" in td_infos[i].extract():
					resume["phone"] = td_temp[0].extract().strip()
					continue
				elif u"所在地区" in td_infos[i].extract():
					resume["living"] = td_temp[0].extract().strip().replace("-", "")
					continue
				elif u"婚姻状况" in td_infos[i].extract():
					resume["marital_status"] = td_temp[0].extract().strip()
					continue
				elif u"参加工作时间" in td_infos[i].extract():
					work_year = td_temp[0].extract().strip()
					if re.match("^\d{4}$", work_year):
						year = str((2016 - int(work_year)) * 12)
						resume["work_year"] = year
					continue
				elif u"最高学历" in td_infos[i].extract():
					resume["degree"] = td_temp[0].extract().strip()
					continue
				elif u"目前状态" in td_infos[i].extract():
					resume["work_status"] = td_temp[0].extract().strip()
					continue


def handle_career_info(resume, info):
	td_infos = info.xpath(".//td[@class='telr']")
	if len(td_infos) > 0:
		for i in range(len(td_infos)):
			td_temp = td_infos[i].xpath("following-sibling::td[1]/text()")
			if len(td_temp) > 0:
				# print td_infos[i].extract()
				if u"期望行业" in td_infos[i].extract():
					resume["expect_industry"] = td_temp[0].extract().strip().replace("·", "/")
					continue
				elif u"期望地点" in td_infos[i].extract():
					resume["expect_city"] = td_temp[0].extract().strip().replace(",", ";")
					continue
				elif u"期望职位" in td_infos[i].extract():
					resume["expect_position"] = td_temp[0].extract().strip()
					continue
				elif u"期望月薪" in td_infos[i].extract():
					salary = td_temp[0].extract().strip()
					if re.match(u"^(\d+) 元/月", salary):
						resume["expect_salary"] = re.match(u"^(\d+) 元/月", salary).group(1)
					continue


def handle_last_salary(resume, info):
	td_infos = info.xpath(".//td[@width='70%']/text()")
	if len(td_infos) > 0:
		last_salary = td_infos[0].extract().strip()
		if re.match(u"^(\d+) 元/月 \* (\d+) 个月", last_salary):
			temp = re.match(u"^(\d+) 元/月 \* (\d+) 个月", last_salary)
			salary = str(int(int(temp.group(1)) * int(temp.group(2)) / 10000))
			resume["last_year_salary"] = salary + "-" + salary + u"万"


# 处理自我评价
def handle_self_intro(resume, info):
	td_infos = info.xpath(".//td")
	if len(td_infos) == 2:
		resume["self_introduction"] = td_infos[1].xpath("string(.)")[0].extract().strip()


def handle_work_exp(resume, info):
	# print len(info)
	for i in range(len(info)):
		# 判断是工作经历而不是项目经历
		if u"公司规模" in info[i].extract() or u"担任职位" in info[i].extract():
			work_list = {"start_date": "", "end_date": "", "experience_desc": "", "enterprise_name": "",
						 "work_time": "", "position_name": "", "enterprise_size": "", "enterprise_industry": "",
						 "enterprise_type": "", "salary": "", "department": "", "second_job_type": "",
						 "first_job_type": ""}
			time_info = info[i].xpath("div[@class='gztime fl']/text()")
			if len(time_info) > 0:
				time_temp = time_info[0].extract().strip()
				if re.match("^(\d{4})\.(\d{2})-(\d{4})\.(\d{2})$", time_temp):
					temp = re.match("^(\d{4})\.(\d{2})-(\d{4})\.(\d{2})$", time_temp)
					work_list["start_date"] = temp.group(1) + "-" + temp.group(2)
					if int(temp.group(3)) > 2020:
						work_list["end_date"] = u"至今"
					else:
						work_list["end_date"] = temp.group(3) + "-" + temp.group(4)
			enter_name_info = info[i].xpath(".//div[@class='gzcomp_title']/text()")
			if len(enter_name_info) > 0:
				work_list["enterprise_name"] = enter_name_info[0].extract().strip()
			enter_info = info[i].xpath(".//div[@class='gzcomp fl']/table//td[@class='telr']")
			for j in range(len(enter_info)):
				if u"公司性质" in enter_info[j].extract():
					enter_type = enter_info[j].xpath("following-sibling::td[1]/text()")
					if len(enter_type) > 0:
						work_list["enterprise_type"] = enter_type[0].extract().strip()
				elif u"公司规模" in enter_info[j].extract():
					enter_size = enter_info[j].xpath("following-sibling::td[1]/text()")
					if len(enter_size) > 0:
						work_list["enterprise_size"] = enter_size[0].extract().strip()
				elif u"所在部门" in enter_info[j].extract():
					department = enter_info[j].xpath("following-sibling::td[1]/text()")
					if len(department) > 0:
						work_list["department"] = department[0].extract().strip()
				elif u"公司行业" in enter_info[j].extract():
					industry = enter_info[j].xpath("following-sibling::td[1]/text()")
					if len(industry) > 0:
						work_list["enterprise_industry"] = industry[0].extract().strip().replace(" ", ",")
				elif u"职位职责" in enter_info[j].extract():
					desc = enter_info[j].xpath("following-sibling::td[1]/text()")
					if len(desc) > 0:
						work_list["experience_desc"] = desc[0].extract().strip().replace("\n", " ")
					if re.search(u"(\d+)年(\d+)个月", work_list["experience_desc"]):
						work_time = re.search(u"(\d+)年(\d+)个月", work_list["experience_desc"])
						work_list["work_time"] = str(int(work_time.group(1)) * 12 + int(work_time.group(2)))
					elif re.search(u"(\d+)个月", work_list["experience_desc"]):
						work_time = re.search(u"(\d+)个月", work_list["experience_desc"])
						work_list["work_time"] = str(work_time.group(1))
				elif u"薪酬状况" in enter_info[j].extract():
					salary = enter_info[j].xpath("following-sibling::td[1]/text()")
					if len(salary) > 0:
						salary_temp = salary[0].extract().strip()
						if re.match(u"(\d+) 元/月", salary_temp):
							work_list["salary"] = re.match(u"(\d+) 元/月", salary_temp).group(1)

			position_info = info[i].xpath(".//div[@class ='wid594 fl']/text()")
			if len(position_info) > 0:
				work_list["position_name"] = position_info[0].extract().strip()

			# 添加到工作经历列表
			if work_list != {"start_date": "", "end_date": "", "experience_desc": "", "enterprise_name": "",
							 "work_time": "", "position_name": "", "enterprise_size": "", "enterprise_industry": "",
							 "enterprise_type": "", "salary": "", "department": "", "second_job_type": "",
							 "first_job_type": ""}:
				resume["workExperienceList"].append(work_list)


def handle_edu_exp(resume, info):
	tr_infos = info.xpath(".//tr")
	if len(tr_infos) > 0:
		for i in range(len(tr_infos)):
			edu_list = {"college_name": "", "profession_name": "", "degree": "", "start_date": "", "end_date": "",
						"desc": ""}
			time_info = tr_infos[i].xpath(".//td[@width='13%']/text()")
			if len(time_info) > 0:
				time_temp = time_info[0].extract().replace("\n", "").strip()
				if re.match("(\d{4})\.(\d{2}) - (\d{4})\.(\d{2})", time_temp):
					temp = re.match("(\d{4})\.(\d{2}) - (\d{4})\.(\d{2})", time_temp)
					edu_list["start_date"] = temp.group(1) + "-" + temp.group(2)
					edu_list["end_date"] = temp.group(3) + "-" + temp.group(4)
			school_info = tr_infos[i].xpath(".//td[@width='30%']/b/text()")
			if len(school_info) > 0:
				edu_list["college_name"] = school_info[0].extract().strip()
			degree_info = tr_infos[i].xpath(".//td[@width='14%']/text()")
			if len(degree_info) > 0:
				edu_list["degree"] = degree_info[0].extract().strip()
			profession_info = tr_infos[i].xpath(".//td[@width='33%']/text()")
			if len(profession_info) > 0:
				edu_list["profession_name"] = profession_info[0].extract().strip()

			# 添加到resume
			if edu_list != {"college_name": "", "profession_name": "", "degree": "", "start_date": "", "end_date": "",
							"desc": ""}:
				resume["educationList"].append(edu_list)


def handle_proj_exp(resume, info):
	if len(info) > 0:
		for i in range(len(info)):
			project_list = {"start_date": "", "end_date": "", "project_name": "", "project_desc": "", "work_desc": "",
							"tools": "", "software": "", "hardware": ""}

			time_info = info[i].xpath("div[@class='gztime fl']/text()")
			if len(time_info) > 0:
				time_temp = time_info[0].extract().strip().replace("\n", "").replace(" ", "")
				if re.match("^(\d{4})\.(\d{2})-(\d{4})\.(\d{2})$", time_temp):
					temp = re.match("^(\d{4})\.(\d{2})-(\d{4})\.(\d{2})$", time_temp)
					project_list["start_date"] = temp.group(1) + "-" + temp.group(2)
					if int(temp.group(3)) > 2020:
						project_list["end_date"] = u"至今"
					else:
						project_list["end_date"] = temp.group(3) + "-" + temp.group(4)
			project_info = info[i].xpath(".//div[@class='gzcomp fl']/table//td[@class='telr']")
			for j in range(len(project_info)):
				if u"项目描述" in project_info[j].extract():
					desc = project_info[j].xpath("following-sibling::td[1]/text()")
					if len(desc) > 0:
						desc_info = desc[0].extract().strip()
						name = re.match("(.+)", desc_info)
						if name:
							project_list["project_name"] = name.group(1).strip()
						soft = re.search(u"软件环境:\n?(.+)", desc_info)
						if soft:
							temp_soft = soft.group(1).strip()
							if ":" in temp_soft:
								soft0 = temp_soft.split(":")
								if len(soft0) > 0 and len(soft0[0]) >= 4:
									temp_soft = soft0[0][:-4]
							project_list["software"] = temp_soft.strip()
						hard = re.search(u"硬件环境:\n?(.+)", desc_info)
						if hard:
							temp_hard = hard.group(1).strip()
							if ":" in temp_hard:
								hard0 = temp_hard.split(":")
								if len(hard0) > 0 and len(hard0[0]) >= 4:
									temp_hard = hard0[0][:-4]
							project_list["hardware"] = temp_hard.strip()
						tools = re.search(u"开发工具:\n?(.+)", desc_info)
						if tools:
							temp_tools = tools.group(1).strip()
							if ":" in temp_tools:
								tools0 = temp_tools.split(":")
								if len(tools0) > 0 and len(tools0[0]) >= 4:
									temp_tools = tools0[0][:-4]
							project_list["tools"] = temp_tools.strip()

						project_list["project_desc"] = desc_info.replace("\n", "").strip()
					break
			# 添加到项目经历
			if project_list != {"start_date": "", "end_date": "", "project_name": "", "project_desc": "",
								"work_desc": "", "tools": "", "software": "", "hardware": ""}:
				resume["projectList"].append(project_list)


def handle_language(resume, info):
	td_info = info.xpath(".//td/text()")

	if len(td_info) == 2:
		lan_infos = td_info[1].extract().strip()
		lan_temp = lan_infos.split(u"、")
		if len(lan_temp) > 0:
			for i in range(len(lan_temp)):
				lan_list = {"language_name": "", "language_ability": "", "language_type": ""}
				lan_list["language_name"] = lan_temp[i]
				# 添加到语言列表
				resume["languageList"].append(lan_list)


def handle_certification(resume, info):
	for i in range(len(info)):
		cert_list = {"get_time": "", "certificate_name": "", "certificate_school": "", "certificate_score": ""}
		time_info = info[i].xpath(".//div[@class='gztime fl']/text()")
		if len(time_info) > 0:
			time_str = time_info[0].extract().strip()
			if re.match("\d{4}-\d{2}", time_str):
				cert_list["get_time"] = time_str
		name_info = info[i].xpath(".//div[@class='gzcomp_title']/text()")
		if len(name_info) > 0:
			cert_list["certificate_name"] = name_info[0].extract().strip()
		school_info = info[i].xpath(".//td[@width='87%']/text()")
		if len(school_info) > 0:
			cert_list["certificate_score"] = school_info[0].extract().strip()
		# 添加到证书列表
		if cert_list != {"get_time": "", "certificate_name": "", "certificate_school": "", "certificate_score": ""}:
			resume["certificateList"].append(cert_list)

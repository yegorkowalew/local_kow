# -*- coding:utf-8 -*-

from lxml import etree, html

f = """
<div class="items-row cols-1 row-0 row-fluid clearfix">
	<div class="span12">
		<div class="item column-1" itemprop="blogPost" itemscope="" itemtype="http://schema.org/BlogPosting">
			<div class="page-header">
				<h2 itemprop="name">
					Підвищення вартості послуг
				</h2>
			</div>
			<dl class="article-info  muted">
				<dt class="article-info-term">
					Деталі
				</dt>
				<dd class="published">
					<span class="icon-calendar"></span>
						<time datetime="2016-03-14T13:00:16+00:00" itemprop="datePublished">14/03/2016</time>
				</dd>
			</dl>
	 			Шановні абоненти!<br>
	 			<br>
	 			З 01.04.2016г. компанія «Ведекон» підвищує вартість наданих послуг:<br>
	 			<br>
	 			- тарифний план 5 Мбіт/1 Мбіт - 200 грн/міс (з ПДВ)<br>
	 			<br>
	 			- тарифний план 2 Мбіт/0,512 Мбіт - 140 грн/міс (з ПДВ)
		</div>
			<!-- end item -->
	</div>
		<!-- end span -->
</div>
"""
from lxml.cssselect import CSSSelector

doc=html.fromstring(f)
# for div in doc.cssselect('div.items-row.cols-1.row-0.row-fluid.clearfix div div div h2'):
    # print(div.text_content())

    #main > div.blog > div.items-row.cols-1.row-0.row-fluid.clearfix > div > div
    #main > div.blog > div.items-row.cols-1.row-0.row-fluid.clearfix > div > div > div > h2
    #main > div.blog > div.items-row.cols-1.row-0.row-fluid.clearfix > div > div > dl > dd
    #main > div.blog > div.items-row.cols-1.row-0.row-fluid.clearfix > div > div > dl > dd > time
    #main > div.blog > div.items-row.cols-1.row-0.row-fluid.clearfix > div > div > d

print(doc.cssselect('div.items-row.cols-1.row-0.row-fluid.clearfix div div div h2')[0].text_content())
print(doc.cssselect('div.items-row.cols-1.row-0.row-fluid.clearfix div div dl dd time')[0].text_content())
# print(doc.cssselect('div.items-row.cols-1.row-0.row-fluid.clearfix div div dl')[0].text_content())
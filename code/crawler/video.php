<?php
#!usr/bin/php
class XiguaVideo
{
	protected $baseUrl = 'https://www.ixigua.com/';
	/**
	 * 获取视频列表
	 */
	public function getVideoList($keyword, $offset = 0, $count = 10)
	{
		$base = $this->baseUrl . 'search_content/';
		$param = [
			'keyword' => $keyword,
 			'format' => 'json',
			'autolaod' => 'true',
			'count' => $count,
			'cur_tab' => 1,
			'offset' => $offset,
		];
		$url = $base . '?' . http_build_query($param);
		//echo $url."\n";
		$data = file_get_contents($url);
		$data = json_decode($data, true);
		$data = $data['data'];
		if(count($data) == 0) { // count($data) == 0
			return false;
		}
		$return = [];
		foreach ($data as $value) {
			$temp = [];
			$temp['video_id'] = (string)$value['id'];
			$temp['title'] = $value['title']; // 标题
			$temp['description'] = $value['abstract']; // 描述
			$temp['keywords'] = $value['keywords']; // 关键字
			$video_page_id = (string)$value['id'];
			//$temp['video_detail_url'] = $this->baseUrl . 'a' . $video_page_id . '/#mid=' . $media_creator_id;''; // 具体视频链接
			$temp['display_url'] = $value['display_url']; // 播放链接
			$temp['source'] = $value['source']; // 来源
			$temp['aothor'] = [ // 相关用户
				'media_creator_id' => $value['media_creator_id'], // 发布人id
				'media_name' => $value['media_name'], // 发布人名字
				'media_url' => 'https://www.cnblogs.com'. $value['media_url'], // 用户链接
			];
			$return[] = $temp;
		}
		return $return;

	}
	/**
	 * 获取视频详情
	 * https://www.ixigua.com/a6482903548135735822/#mid=50433819368
	 * https://www.cnblogs.com/cwl168/p/3819559.html
	 * 正则小心换行符
	 */
	public function getVideoDetail($video_page_id, $media_creator_id)
	{
		$base = $this->baseUrl . 'a' . $video_page_id . '/#mid=' . $media_creator_id;
		$data = file_get_contents($base);
		// 解析数据
		$pattern = '/abstractInfo:([\s\S]*?)commentInfo/s';
		preg_match_all($pattern, $data, $match);
		// {
		  //     isOriginal: true,
		  //     title: '中国非遗：苏州评弹',
		  //     content: '&lt;p&gt;&lt;/p&gt;&lt;p&gt;中国非遗：苏州评弹。为加快传承，视频上传时选用原创功能。新地理，中国非遗与地理标志性文化传承平台。&lt;/p&gt;',
		  //     mediaUrl: '/c/user/50433819368/',
		  //     mediaId: '50433819368',
		  //     avatarUrl: 'https://p1.pstatp.com/thumb/d2a0016a82e6c7c368e',
		  //     name: '新地理',
		  //     videoPlayCount: 18805,
		  //     follow: false,
		  //     isSelf: false,
		  //     groupId: '6482903548135735822'
  		  //   },
		$data = $match[1][0];
		// 获取标题
		$title = $this->getBetween($data, 'title:', 'content');
		$title = trim(trim(trim($title), ','), '\''); // 去除空格 单引号 半角逗号
		// 获取内容
		$content = $this->getBetween($data, 'content:', 'mediaUrl');
		$content = str_replace(PHP_EOL, '', $content);
		$content = trim($content);
		$content = trim($content, ',');
		$content = trim($content, '\'');
		// 获取这个用户的链接
		$mediaUrl = $this->getBetween($data, 'mediaUrl:', 'mediaId');
		$mediaUrl = trim(trim(trim($mediaUrl), ','), '\''); // 去除空格 单引号 半角逗号		
		// 返回数据
		$return = [];
		$return['title'] = $title;
		$return['content'] = $content;
		$return['original_video_detail_url'] = $base;
		$return['media_url'] = $mediaUrl;
		return $return;

	}
	/**
	 * 解析JS文本字符串
	 */
	private function getBetween($input, $start, $end)
	{
		$substr = substr($input, strlen($start)+strpos($input, $start),(strlen($input) - strpos($input, $end))*(-1));
   		return $substr;		
	}

}
// $put_feiyi_data = [];
// $data = ['a' => 1];
// $put_feiyi_data = array_merge($put_feiyi_data, $data);
// var_dump($put_feiyi_data);
// die;
// $data = file_get_contents('https://www.ixigua.com/search_content/?format=json&autoload=true&count=20&keyword=非遗&cur_tab=1&offset=180');
// $data = json_decode($data, true);
// $data = $data['data'];
// var_dump($data);
// die;
$t1 = microtime(true);
$xigua = new XiguaVideo;
// $detail = $xigua->getVideoDetail('6482903548135735822', '50433819368');
// [[]]
// var_dump($detail);
// $data = $xigua->getVideoList('非遗');
// file_put_contents('../dataset/video_info.json', json_encode($data, 320));
$offset = 0;
$count = 20; // 每页的数目
$data = $xigua->getVideoList('非遗', $offset, $count);
file_put_contents("../dataset/feiyi/{$offset}.json", json_encode($data, 320));
$put_feiyi_data = [];
while($data !== false) {
	echo count($data)."非遗-{$offset}\n";
	//sleep(1);
	$offset += $count;
	$data = $xigua->getVideoList('非遗', $offset, $count); 
	echo $data[0]['title']."\n";
	//echo gettype($data)."\n";
	if(is_array($data)) {
		$put_feiyi_data = array_merge($put_feiyi_data, $data);
	}
	file_put_contents("../dataset/feiyi/{$offset}.json", json_encode($data, 320));
}

echo '非遗完毕';
echo "\n";
file_put_contents('../dataset/feiyi_video_info.json', json_encode($put_feiyi_data, 320));


$offset = 0;
$data = $xigua->getVideoList('非物质文化遗产', $offset, $count);
file_put_contents("../dataset/feiwuzhiwenhuayichan/{$offset}.json", json_encode($data, 320));
$put_feiwuzhiwenhuayichan_data = [];

while($data !== false) {
	echo count($data)."非物质文化遗产-{$offset}\n";
	//sleep(1);
	$offset += $count;
	$data = $xigua->getVideoList('非物质文化遗产', $offset, $count);
	echo $data[0]['title']."\n"; 
	if(is_array($data)) {	
		$put_feiwuzhiwenhuayichan_data = array_merge($put_feiwuzhiwenhuayichan_data, $data);
	}
	file_put_contents("../dataset/feiwuzhiwenhuayichan/{$offset}.json", json_encode($data, 320));
}
echo '非物质文化遗完毕';
echo "\n";
file_put_contents('../dataset/feiwuzhiwenhuayichan_video_info.json', json_encode($put_feiwuzhiwenhuayichan_data, 320));
echo '合并';
echo "\n";
$put_feiwuzhiwenhuayichan_data = array_merge($put_feiwuzhiwenhuayichan_data, $put_feiyi_data);
file_put_contents('../dataset/video_info.json', json_encode($put_feiwuzhiwenhuayichan_data, 320));

$t2 = microtime(true);
echo '耗时'.round($t2-$t1,3).'秒、';


//	滚动触发动效插件
//	依赖 jquery、tweenmax、throttle-debounce
//	attr: x y scale rotation skewX skewY xPercent yPercent autoAlpha delay repeat repeatDelay yoyo force3D transformOrigin perspective *cycle *overwrite
//	Linear, Back, Bounce, Circ, Cubic, Ease, EaseLookUp, Elastic, Expo, Power0, Power1, Power2, Power3, Power4, Quad, Quart, Quint, Sine, Strong, SlowMo, Stepped
//	ease.easeIn, ease.easeOut, ease.easeInOut

;(function($){
	$.fn.xRoll = function(opt){
		var def = {
			xclass: 'xtween',						// 到达触发点class
			throttle: 250,							// 节流频率，默认250毫秒
			debounce: 250,							// 去抖频率，默认250毫秒
			mobile: false,							// 是否支持移动端
			ie8: 1,											// 是否支持ie8 0-完全不支持 1-不支持插件动画（支持触发xclass及回调函数） 2-不支持插件动画及触发xclass（仅支持回调函数） 3-不支持插件动画及回调函数（仅支持触发xclass） 4-完全支持
			offset: 0,									// 触发点偏移(px)
			ratio: 0.3,									// 触发于视口高度的比例位置，默认视口垂直中点(如果滚动到页面底部仍无法触发此值，内部会计算一个临界值覆盖此值，以保证元素最终会移动到指定位置)
			stepmode: false,						// 设定运动模式，默认到达触发点自行运动，true-步进模式运动
			duration: 1,								// 设定动画持续时间，默认1秒
			stagger: -1,								// target: true 时作用于子元素运动间隔时间，默认 序列运动
			target: false,							// 以父级位置触发子级动画 true-所有子元素，false-自身，css选择器-选中的子集
			trans: {},									// 设定动画动作
			onRoll: function(elm,rate){},		// 回调函数
			onIn: function(elm){},			// 回调函数
			onOut: function(elm){}			// 回调函数
		};
			
		var opt = $.extend(def, opt);
		
		var wheight = $(window).height();
		var bheight = $('body').height();
		var wstop = $(window).scrollTop();
		
		this.each(function(i){
			var _this = $(this);
			
			if(typeof(_this.data('xr-progress')) !== "undefined"){
				console.log('[xRoll] 重复调用！');
				return;
			}else{
				_this.data('xr-progress', 0);
			}
			
			var _attr = {
				idx: i,
				height: _this.outerHeight(),
				top: _this.offset().top,
				progress: 0,
//				获取自定义属性值
				mobile: _this.data('xr-mobile') || opt.mobile,
				ie8: typeof(_this.data('xr-ie8')) !== "undefined" ? _this.data('xr-ie8') : opt.ie8,
				offset: _this.data('xr-offset') || opt.offset,
				ratio: _this.data('xr-ratio') || opt.ratio,
				stepmode: _this.data('xr-stepmode') || opt.stepmode,
				duration: _this.data('xr-duration') || opt.duration,
				stagger: _this.data('xr-stagger') >= 0 ? _this.data('xr-stagger') : opt.stagger,
				target: _this.data('xr-target') || opt.target,
				trans: !!_this.data('xr-trans') ? eval('(' + _this.data('xr-trans') + ')') : {}
			};
			
			if(!$.support.leadingWhitespace && !_attr.ie8) return;

			if(!_attr.mobile && device().isMobile) return;
			
			if(_attr.ratio > (bheight - _attr.top + _attr.offset)/wheight){
				_attr.ratio = (bheight - _attr.top + _attr.offset)/wheight;
			}

			if(_attr.stagger < 0){
				_attr.stagger = _attr.trans.delay ? _attr.duration + _attr.trans.delay : _attr.stagger = _attr.duration;
			}
			
			_attr.trans = _attr.trans.autoAlpha ? $.extend({}, true, opt.trans, _attr.trans) : $.extend({autoAlpha: 0}, true, opt.trans, _attr.trans);
			
			if(!$.support.leadingWhitespace && _attr.ie8 < 4){
				_attr.trans =  $.extend({}, _attr.trans, {autoAlpha: 1});
				console.log(_attr.trans);
			}
			
			$(window).on('load', function(){
				var _tm = new TimelineMax();
				
				if(_attr.stepmode){
					opt.throttle = 0;
				}
				
				Init(_tm);
				
				var throttled = null, debounced = null;
				if(opt.throttle > 0){
					throttled = $.throttle(opt.throttle, function(){
						scrollFn(_this, _attr, _tm);
					});
				}else{
					throttled = function(){
						scrollFn(_this, _attr, _tm);
					};
				}

				if(opt.debounce > 0){
					debounced = $.debounce(opt.debounce, function(){
						wheight = $(window).height();
						bheight = $('body').height();
						wstop = $(window).scrollTop();

						scrollFn(_this, _attr, _tm);
					});
				}else{
					debounced = function(){
						wheight = $(window).height();
						bheight = $('body').height();
						wstop = $(window).scrollTop();

						scrollFn(_this, _attr, _tm);
					};
				}

				$(window).on('scroll', throttled);
				$(window).on('resize orientationchange', debounced);
				
			});
			
			function Init(tm){
				wheight = $(window).height();
				bheight = $('body').height();
				wstop = $(window).scrollTop();

				_attr.height = _this.outerHeight();
				_attr.top = _this.offset().top;

				if(_attr.ratio > (bheight - _attr.top + _attr.offset)/wheight){
					_attr.ratio = (bheight - _attr.top + _attr.offset)/wheight;
				}
				
	//				判断如果是父级就运动其子集或指定后代，否则运动元素自身
				if(_attr.target){
					if(typeof _attr.target == 'boolean'){
						tm.staggerFrom(_this.children(), _attr.duration, _attr.trans, _attr.stagger);
					}else if(typeof _attr.target == 'string'){
						tm.staggerFrom(_this.find(_attr.target), _attr.duration, _attr.trans, _attr.stagger);
					}
				}else{
					tm.from(_this, _attr.duration, _attr.trans);
				}
				tm.stop();
				
				scrollFn(_this, _attr, tm);
			}

		});
		
		function scrollFn(ele, attr, tm){
			wstop = $(window).scrollTop();

			attr.progress = (wstop + wheight - attr.top + attr.offset) / (wheight * attr.ratio);
			ele.data('xr-progress', attr.progress);
			opt.onRoll(ele, attr.progress);

			if(attr.stepmode){
				if(attr.progress < 0){
					if(ele.hasClass(opt.xclass)){
							if(!$.support.leadingWhitespace){
								switch(attr.ie8){
									case 2:
										opt.onOut(ele);
										break;
									case 3:
										ele.removeClass(opt.xclass);
										break;
									default:
										ele.removeClass(opt.xclass);
										opt.onOut(ele);
									}
							}else{
								ele.removeClass(opt.xclass);
								opt.onOut(ele);
							}
					}
					if(!$.support.leadingWhitespace){
						if(attr.ie8 > 3){
							tm.progress(0);
						}
					}else{
						tm.progress(0);
					}
				}else{
					if(attr.progress > 1){
						if(!ele.hasClass(opt.xclass)){
							if(!$.support.leadingWhitespace){
								switch(attr.ie8){
									case 2:
										opt.onIn(ele);
										break;
									case 3:
										ele.addClass(opt.xclass);
										break;
									default:
										ele.addClass(opt.xclass);
										opt.onIn(ele);
									}
							}else{
								ele.addClass(opt.xclass);
								opt.onIn(ele);
							}
						}
						if(!$.support.leadingWhitespace){
							if(attr.ie8 > 3){
								tm.progress(1);
							}
						}else{
							tm.progress(1);
						}
					}else{
						if(!$.support.leadingWhitespace){
							if(attr.ie8 > 3){
								tm.progress(attr.progress);
							}
						}else{
							tm.progress(attr.progress);
						}
					}
				}
			}else{
				if(!ele.hasClass(opt.xclass)){
					if(attr.progress >= 1){
						if(!$.support.leadingWhitespace){
							switch(attr.ie8){
								case 1:
									ele.addClass(opt.xclass);
									opt.onIn(ele);
									break;
								case 2:
									opt.onIn(ele);
									break;
								case 3:
									ele.addClass(opt.xclass);
									break;
								default:
									ele.addClass(opt.xclass);
									tm.play();
									opt.onIn(ele);
								}
						}else{
							ele.addClass(opt.xclass);
							tm.play();
							opt.onIn(ele);
						}
					}
				}else{
					if(attr.progress < 0.1){
						if(!$.support.leadingWhitespace){
							switch(attr.ie8){
								case 1:
									ele.removeClass(opt.xclass);
									opt.onOut(ele);
									break;
								case 2:
									opt.onOut(ele);
									break;
								case 3:
									ele.removeClass(opt.xclass);
									break;
								default:
									ele.removeClass(opt.xclass);
									tm.reverse();
									opt.onOut(ele);
								}
						}else{
							ele.removeClass(opt.xclass);
							tm.reverse();
							opt.onOut(ele);
						}
					}
				}
			}
		}
				
		return this;
	};
})(jQuery);
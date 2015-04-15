


<!DOCTYPE html>
<html lang="en" class="">
  <head prefix="og: http://ogp.me/ns# fb: http://ogp.me/ns/fb# object: http://ogp.me/ns/object# article: http://ogp.me/ns/article# profile: http://ogp.me/ns/profile#">
    <meta charset='utf-8'>
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta http-equiv="Content-Language" content="en">
    
    
    <title>bayesian-itc/models.py at racemic_mixture · CCBatIIT/bayesian-itc</title>
    <link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="GitHub">
    <link rel="fluid-icon" href="https://github.com/fluidicon.png" title="GitHub">
    <link rel="apple-touch-icon" sizes="57x57" href="/apple-touch-icon-114.png">
    <link rel="apple-touch-icon" sizes="114x114" href="/apple-touch-icon-114.png">
    <link rel="apple-touch-icon" sizes="72x72" href="/apple-touch-icon-144.png">
    <link rel="apple-touch-icon" sizes="144x144" href="/apple-touch-icon-144.png">
    <meta property="fb:app_id" content="1401488693436528">

      <meta content="@github" name="twitter:site" /><meta content="summary" name="twitter:card" /><meta content="CCBatIIT/bayesian-itc" name="twitter:title" /><meta content="bayesian-itc - Python tools for the analysis and modeling of isothermal titration calorimetry (ITC) experiments." name="twitter:description" /><meta content="https://avatars2.githubusercontent.com/u/6304832?v=3&amp;s=400" name="twitter:image:src" />
      <meta content="GitHub" property="og:site_name" /><meta content="object" property="og:type" /><meta content="https://avatars2.githubusercontent.com/u/6304832?v=3&amp;s=400" property="og:image" /><meta content="CCBatIIT/bayesian-itc" property="og:title" /><meta content="https://github.com/CCBatIIT/bayesian-itc" property="og:url" /><meta content="bayesian-itc - Python tools for the analysis and modeling of isothermal titration calorimetry (ITC) experiments." property="og:description" />
      <meta name="browser-stats-url" content="https://api.github.com/_private/browser/stats">
    <meta name="browser-errors-url" content="https://api.github.com/_private/browser/errors">
    <link rel="assets" href="https://assets-cdn.github.com/">
    <link rel="web-socket" href="wss://live.github.com/_sockets/NjMwNDgyNDo4OWU3NTBhOWViMmJkY2YyMjMxYWUzNGZlNDFkMmUyYTpiMWE3NWRlMTg5MjAxM2MzYzllZGQzYWNiYzU5NmY2MzhlZjMxNTVhMzQ4OWJjODM3ODc1ZTBlZWRmOTBkNTQ2--4f93483171548be22e07ee32415812d9c778f8ef">
    <meta name="pjax-timeout" content="1000">
    <link rel="sudo-modal" href="/sessions/sudo_modal">

    <meta name="msapplication-TileImage" content="/windows-tile.png">
    <meta name="msapplication-TileColor" content="#ffffff">
    <meta name="selected-link" value="repo_source" data-pjax-transient>
      <meta name="google-analytics" content="UA-3769691-2">

    <meta content="collector.githubapp.com" name="octolytics-host" /><meta content="collector-cdn.github.com" name="octolytics-script-host" /><meta content="github" name="octolytics-app-id" /><meta content="68C26441:5906:C0A7666:552E7CE3" name="octolytics-dimension-request_id" /><meta content="6304824" name="octolytics-actor-id" /><meta content="daveminh" name="octolytics-actor-login" /><meta content="82923ce4555df867d892aff8dde39f905af14a8e55749fb15fdc1a48f36b83f1" name="octolytics-actor-hash" />
    
    <meta content="Rails, view, blob#show" name="analytics-event" />
    <meta class="js-ga-set" name="dimension1" content="Logged In">
    <meta class="js-ga-set" name="dimension2" content="Header v3">
    <meta name="is-dotcom" content="true">
    <meta name="hostname" content="github.com">
    <meta name="user-login" content="daveminh">

    
    <link rel="icon" type="image/x-icon" href="https://assets-cdn.github.com/favicon.ico">


    <meta content="authenticity_token" name="csrf-param" />
<meta content="bOyNqKwqtpS8h3WZaXp7jT7lR7rkXDrTy2kuykNZPu2yl5udSgCJtIgvcW2OsfjtBSe7634NdTDsj2BiClCDgw==" name="csrf-token" />

    <link href="https://assets-cdn.github.com/assets/github-02784141552211464e1159c492ceb9c75d7b9baba877522f68faccb088699614.css" media="all" rel="stylesheet" />
    <link href="https://assets-cdn.github.com/assets/github2-3835cf60ca9c7d6f833ba80470859e417a7c0da9cc572ecb2c36ae79b2234332.css" media="all" rel="stylesheet" />
    
    


    <meta http-equiv="x-pjax-version" content="be127a1bc145075f45563e8af963c3fb">

      
  <meta name="description" content="bayesian-itc - Python tools for the analysis and modeling of isothermal titration calorimetry (ITC) experiments.">
  <meta name="go-import" content="github.com/CCBatIIT/bayesian-itc git https://github.com/CCBatIIT/bayesian-itc.git">

  <meta content="6304832" name="octolytics-dimension-user_id" /><meta content="CCBatIIT" name="octolytics-dimension-user_login" /><meta content="23921280" name="octolytics-dimension-repository_id" /><meta content="CCBatIIT/bayesian-itc" name="octolytics-dimension-repository_nwo" /><meta content="true" name="octolytics-dimension-repository_public" /><meta content="true" name="octolytics-dimension-repository_is_fork" /><meta content="14320910" name="octolytics-dimension-repository_parent_id" /><meta content="choderalab/bayesian-itc" name="octolytics-dimension-repository_parent_nwo" /><meta content="14320910" name="octolytics-dimension-repository_network_root_id" /><meta content="choderalab/bayesian-itc" name="octolytics-dimension-repository_network_root_nwo" />
  <link href="https://github.com/CCBatIIT/bayesian-itc/commits/racemic_mixture.atom" rel="alternate" title="Recent Commits to bayesian-itc:racemic_mixture" type="application/atom+xml">

  </head>


  <body class="logged_in  env-production macintosh vis-public fork page-blob">
    <a href="#start-of-content" tabindex="1" class="accessibility-aid js-skip-to-content">Skip to content</a>
    <div class="wrapper">
      
      
      


        <div class="header header-logged-in true" role="banner">
  <div class="container clearfix">

    <a class="header-logo-invertocat" href="https://github.com/" data-hotkey="g d" aria-label="Homepage" data-ga-click="Header, go to dashboard, icon:logo">
  <span class="mega-octicon octicon-mark-github"></span>
</a>


      <div class="site-search repo-scope js-site-search" role="search">
          <form accept-charset="UTF-8" action="/CCBatIIT/bayesian-itc/search" class="js-site-search-form" data-global-search-url="/search" data-repo-search-url="/CCBatIIT/bayesian-itc/search" method="get"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /></div>
  <input type="text"
    class="js-site-search-field is-clearable"
    data-hotkey="s"
    name="q"
    placeholder="Search"
    data-global-scope-placeholder="Search GitHub"
    data-repo-scope-placeholder="Search"
    tabindex="1"
    autocapitalize="off">
  <div class="scope-badge">This repository</div>
</form>
      </div>

      <ul class="header-nav left" role="navigation">
          <li class="header-nav-item explore">
            <a class="header-nav-link" href="/explore" data-ga-click="Header, go to explore, text:explore">Explore</a>
          </li>
            <li class="header-nav-item">
              <a class="header-nav-link" href="https://gist.github.com" data-ga-click="Header, go to gist, text:gist">Gist</a>
            </li>
            <li class="header-nav-item">
              <a class="header-nav-link" href="/blog" data-ga-click="Header, go to blog, text:blog">Blog</a>
            </li>
          <li class="header-nav-item">
            <a class="header-nav-link" href="https://help.github.com" data-ga-click="Header, go to help, text:help">Help</a>
          </li>
      </ul>

      
<ul class="header-nav user-nav right" id="user-links">
  <li class="header-nav-item dropdown js-menu-container">
    <a class="header-nav-link name" href="/daveminh" data-ga-click="Header, go to profile, text:username">
      <img alt="@daveminh" class="avatar" data-user="6304824" height="20" src="https://avatars1.githubusercontent.com/u/6304824?v=3&amp;s=40" width="20" />
      <span class="css-truncate">
        <span class="css-truncate-target">daveminh</span>
      </span>
    </a>
  </li>

  <li class="header-nav-item dropdown js-menu-container">
    <a class="header-nav-link js-menu-target tooltipped tooltipped-s" href="/new" aria-label="Create new..." data-ga-click="Header, create new, icon:add">
      <span class="octicon octicon-plus"></span>
      <span class="dropdown-caret"></span>
    </a>

    <div class="dropdown-menu-content js-menu-content">
      <ul class="dropdown-menu">
        
<li>
  <a href="/new" data-ga-click="Header, create new repository, icon:repo"><span class="octicon octicon-repo"></span> New repository</a>
</li>
<li>
  <a href="/organizations/new" data-ga-click="Header, create new organization, icon:organization"><span class="octicon octicon-organization"></span> New organization</a>
</li>
  <li class="dropdown-divider"></li>
  <li class="dropdown-header">
    <span title="CCBatIIT">This organization</span>
  </li>

  <li>
    <a href="/orgs/CCBatIIT/invitations/new" data-ga-click="Header, invite someone, icon:person"><span class="octicon octicon-person"></span> Invite someone</a>
  </li>

  <li>
    <a href="/orgs/CCBatIIT/new-team" data-ga-click="Header, create new team, icon:jersey"><span class="octicon octicon-jersey"></span> New team</a>
  </li>

  <li>
    <a href="/organizations/CCBatIIT/repositories/new" data-ga-click="Header, create new organization repository, icon:repo"><span class="octicon octicon-repo"></span> New repository</a>
  </li>


  <li class="dropdown-divider"></li>
  <li class="dropdown-header">
    <span title="CCBatIIT/bayesian-itc">This repository</span>
  </li>
    <li>
      <a href="/CCBatIIT/bayesian-itc/settings/collaboration" data-ga-click="Header, create new collaborator, icon:person"><span class="octicon octicon-person"></span> New collaborator</a>
    </li>

      </ul>
    </div>
  </li>

  <li class="header-nav-item">
        <a href="/notifications" aria-label="You have unread notifications" class="header-nav-link notification-indicator tooltipped tooltipped-s" data-ga-click="Header, go to notifications, icon:unread" data-hotkey="g n">
        <span class="mail-status unread"></span>
        <span class="octicon octicon-inbox"></span>
</a>
  </li>

  <li class="header-nav-item">
    <a class="header-nav-link tooltipped tooltipped-s" href="/settings/profile" id="account_settings" aria-label="Settings" data-ga-click="Header, go to settings, icon:settings">
      <span class="octicon octicon-gear"></span>
    </a>
  </li>

  <li class="header-nav-item">
    <form accept-charset="UTF-8" action="/logout" class="logout-form" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="GvKMgypqbw4XT5q0lupy3rvFXRWCQkFZ6cenyjUcCH3a4mnmwemaunPmfiA0U51SCnHwGhJ8N/QzdpmWcqIhgw==" /></div>
      <button class="header-nav-link sign-out-button tooltipped tooltipped-s" aria-label="Sign out" data-ga-click="Header, sign out, icon:logout">
        <span class="octicon octicon-sign-out"></span>
      </button>
</form>  </li>

</ul>



    
  </div>
</div>

        

        


      <div id="start-of-content" class="accessibility-aid"></div>
          <div class="site" itemscope itemtype="http://schema.org/WebPage">
    <div id="js-flash-container">
      
    </div>
    <div class="pagehead repohead instapaper_ignore readability-menu">
      <div class="container">
        
<ul class="pagehead-actions">

  <li>
      <form accept-charset="UTF-8" action="/notifications/subscribe" class="js-social-container" data-autosubmit="true" data-remote="true" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="mXW171h6yjfk8EJG1pHNfxPRh9SyFehLGzMwBRxPeaPyBHlqahQHdLKfJT/cKMpPc/OblYQk1va3CHfNNpQ8nA==" /></div>    <input id="repository_id" name="repository_id" type="hidden" value="23921280" />

      <div class="select-menu js-menu-container js-select-menu">
        <a href="/CCBatIIT/bayesian-itc/subscription"
          class="btn btn-sm btn-with-count select-menu-button js-menu-target" role="button" tabindex="0" aria-haspopup="true"
          data-ga-click="Repository, click Watch settings, action:blob#show">
          <span class="js-select-button">
            <span class="octicon octicon-eye"></span>
            Unwatch
          </span>
        </a>
        <a class="social-count js-social-count" href="/CCBatIIT/bayesian-itc/watchers">
          4
        </a>

        <div class="select-menu-modal-holder">
          <div class="select-menu-modal subscription-menu-modal js-menu-content" aria-hidden="true">
            <div class="select-menu-header">
              <span class="select-menu-title">Notifications</span>
              <span class="octicon octicon-x js-menu-close" role="button" aria-label="Close"></span>
            </div>

            <div class="select-menu-list js-navigation-container" role="menu">

              <div class="select-menu-item js-navigation-item " role="menuitem" tabindex="0">
                <span class="select-menu-item-icon octicon octicon-check"></span>
                <div class="select-menu-item-text">
                  <input id="do_included" name="do" type="radio" value="included" />
                  <span class="select-menu-item-heading">Not watching</span>
                  <span class="description">Be notified when participating or @mentioned.</span>
                  <span class="js-select-button-text hidden-select-button-text">
                    <span class="octicon octicon-eye"></span>
                    Watch
                  </span>
                </div>
              </div>

              <div class="select-menu-item js-navigation-item selected" role="menuitem" tabindex="0">
                <span class="select-menu-item-icon octicon octicon octicon-check"></span>
                <div class="select-menu-item-text">
                  <input checked="checked" id="do_subscribed" name="do" type="radio" value="subscribed" />
                  <span class="select-menu-item-heading">Watching</span>
                  <span class="description">Be notified of all conversations.</span>
                  <span class="js-select-button-text hidden-select-button-text">
                    <span class="octicon octicon-eye"></span>
                    Unwatch
                  </span>
                </div>
              </div>

              <div class="select-menu-item js-navigation-item " role="menuitem" tabindex="0">
                <span class="select-menu-item-icon octicon octicon-check"></span>
                <div class="select-menu-item-text">
                  <input id="do_ignore" name="do" type="radio" value="ignore" />
                  <span class="select-menu-item-heading">Ignoring</span>
                  <span class="description">Never be notified.</span>
                  <span class="js-select-button-text hidden-select-button-text">
                    <span class="octicon octicon-mute"></span>
                    Stop ignoring
                  </span>
                </div>
              </div>

            </div>

          </div>
        </div>
      </div>
</form>
  </li>

  <li>
    
  <div class="js-toggler-container js-social-container starring-container ">

    <form accept-charset="UTF-8" action="/CCBatIIT/bayesian-itc/unstar" class="js-toggler-form starred js-unstar-button" data-remote="true" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="BxbpLoAHEjjrTC0j0/X9HDN1G2ZpkmMxkd2dHWvYYm4GkKpZx9eeGYxYbjExeistaZK7C0IS8jkglnBLMNFYEA==" /></div>
      <button
        class="btn btn-sm btn-with-count js-toggler-target"
        aria-label="Unstar this repository" title="Unstar CCBatIIT/bayesian-itc"
        data-ga-click="Repository, click unstar button, action:blob#show; text:Unstar">
        <span class="octicon octicon-star"></span>
        Unstar
      </button>
        <a class="social-count js-social-count" href="/CCBatIIT/bayesian-itc/stargazers">
          0
        </a>
</form>
    <form accept-charset="UTF-8" action="/CCBatIIT/bayesian-itc/star" class="js-toggler-form unstarred js-star-button" data-remote="true" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="1FnCy3CqhXz12OSf2ZDHeHK7M4PN5dGd00gP65yl/bFi0efjJd7OM8lk1O9JisjpzYQl2/D4XytHm4Qv1pQUYw==" /></div>
      <button
        class="btn btn-sm btn-with-count js-toggler-target"
        aria-label="Star this repository" title="Star CCBatIIT/bayesian-itc"
        data-ga-click="Repository, click star button, action:blob#show; text:Star">
        <span class="octicon octicon-star"></span>
        Star
      </button>
        <a class="social-count js-social-count" href="/CCBatIIT/bayesian-itc/stargazers">
          0
        </a>
</form>  </div>

  </li>

        <li>
          <a href="#fork-destination-box" class="btn btn-sm btn-with-count"
              title="Fork your own copy of CCBatIIT/bayesian-itc to your account"
              aria-label="Fork your own copy of CCBatIIT/bayesian-itc to your account"
              rel="facebox"
              data-ga-click="Repository, show fork modal, action:blob#show; text:Fork">
            <span class="octicon octicon-repo-forked"></span>
            Fork
          </a>
          <a href="/CCBatIIT/bayesian-itc/network" class="social-count">5</a>

          <div id="fork-destination-box" style="display: none;">
            <h2 class="facebox-header">Where should we fork this repository?</h2>
            <include-fragment src=""
                class="js-fork-select-fragment fork-select-fragment"
                data-url="/CCBatIIT/bayesian-itc/fork?fragment=1">
              <img alt="Loading" height="64" src="https://assets-cdn.github.com/assets/spinners/octocat-spinner-128-338974454bb5c32803e82f601beb051d373744b024fe8742a76009700fd7e033.gif" width="64" />
            </include-fragment>
          </div>
        </li>

</ul>

        <h1 itemscope itemtype="http://data-vocabulary.org/Breadcrumb" class="entry-title public">
          <span class="mega-octicon octicon-repo-forked"></span>
          <span class="author"><a href="/CCBatIIT" class="url fn" itemprop="url" rel="author"><span itemprop="title">CCBatIIT</span></a></span><!--
       --><span class="path-divider">/</span><!--
       --><strong><a href="/CCBatIIT/bayesian-itc" class="js-current-repository" data-pjax="#js-repo-pjax-container">bayesian-itc</a></strong>

          <span class="page-context-loader">
            <img alt="" height="16" src="https://assets-cdn.github.com/assets/spinners/octocat-spinner-32-e513294efa576953719e4e2de888dd9cf929b7d62ed8d05f25e731d02452ab6c.gif" width="16" />
          </span>

            <span class="fork-flag">
              <span class="text">forked from <a href="/choderalab/bayesian-itc">choderalab/bayesian-itc</a></span>
            </span>
        </h1>
      </div><!-- /.container -->
    </div><!-- /.repohead -->

    <div class="container">
      <div class="repository-with-sidebar repo-container new-discussion-timeline  ">
        <div class="repository-sidebar clearfix">
            
<nav class="sunken-menu repo-nav js-repo-nav js-sidenav-container-pjax js-octicon-loaders"
     role="navigation"
     data-pjax="#js-repo-pjax-container"
     data-issue-count-url="/CCBatIIT/bayesian-itc/issues/counts">
  <ul class="sunken-menu-group">
    <li class="tooltipped tooltipped-w" aria-label="Code">
      <a href="/CCBatIIT/bayesian-itc" aria-label="Code" class="selected js-selected-navigation-item sunken-menu-item" data-hotkey="g c" data-selected-links="repo_source repo_downloads repo_commits repo_releases repo_tags repo_branches /CCBatIIT/bayesian-itc">
        <span class="octicon octicon-code"></span> <span class="full-word">Code</span>
        <img alt="" class="mini-loader" height="16" src="https://assets-cdn.github.com/assets/spinners/octocat-spinner-32-e513294efa576953719e4e2de888dd9cf929b7d62ed8d05f25e731d02452ab6c.gif" width="16" />
</a>    </li>


    <li class="tooltipped tooltipped-w" aria-label="Pull requests">
      <a href="/CCBatIIT/bayesian-itc/pulls" aria-label="Pull requests" class="js-selected-navigation-item sunken-menu-item" data-hotkey="g p" data-selected-links="repo_pulls /CCBatIIT/bayesian-itc/pulls">
          <span class="octicon octicon-git-pull-request"></span> <span class="full-word">Pull requests</span>
          <span class="js-pull-replace-counter"></span>
          <img alt="" class="mini-loader" height="16" src="https://assets-cdn.github.com/assets/spinners/octocat-spinner-32-e513294efa576953719e4e2de888dd9cf929b7d62ed8d05f25e731d02452ab6c.gif" width="16" />
</a>    </li>

      <li class="tooltipped tooltipped-w" aria-label="Wiki">
        <a href="/CCBatIIT/bayesian-itc/wiki" aria-label="Wiki" class="js-selected-navigation-item sunken-menu-item" data-hotkey="g w" data-selected-links="repo_wiki /CCBatIIT/bayesian-itc/wiki">
          <span class="octicon octicon-book"></span> <span class="full-word">Wiki</span>
          <img alt="" class="mini-loader" height="16" src="https://assets-cdn.github.com/assets/spinners/octocat-spinner-32-e513294efa576953719e4e2de888dd9cf929b7d62ed8d05f25e731d02452ab6c.gif" width="16" />
</a>      </li>
  </ul>
  <div class="sunken-menu-separator"></div>
  <ul class="sunken-menu-group">

    <li class="tooltipped tooltipped-w" aria-label="Pulse">
      <a href="/CCBatIIT/bayesian-itc/pulse" aria-label="Pulse" class="js-selected-navigation-item sunken-menu-item" data-selected-links="pulse /CCBatIIT/bayesian-itc/pulse">
        <span class="octicon octicon-pulse"></span> <span class="full-word">Pulse</span>
        <img alt="" class="mini-loader" height="16" src="https://assets-cdn.github.com/assets/spinners/octocat-spinner-32-e513294efa576953719e4e2de888dd9cf929b7d62ed8d05f25e731d02452ab6c.gif" width="16" />
</a>    </li>

    <li class="tooltipped tooltipped-w" aria-label="Graphs">
      <a href="/CCBatIIT/bayesian-itc/graphs" aria-label="Graphs" class="js-selected-navigation-item sunken-menu-item" data-selected-links="repo_graphs repo_contributors /CCBatIIT/bayesian-itc/graphs">
        <span class="octicon octicon-graph"></span> <span class="full-word">Graphs</span>
        <img alt="" class="mini-loader" height="16" src="https://assets-cdn.github.com/assets/spinners/octocat-spinner-32-e513294efa576953719e4e2de888dd9cf929b7d62ed8d05f25e731d02452ab6c.gif" width="16" />
</a>    </li>
  </ul>


    <div class="sunken-menu-separator"></div>
    <ul class="sunken-menu-group">
      <li class="tooltipped tooltipped-w" aria-label="Settings">
        <a href="/CCBatIIT/bayesian-itc/settings" aria-label="Settings" class="js-selected-navigation-item sunken-menu-item" data-selected-links="repo_settings /CCBatIIT/bayesian-itc/settings">
          <span class="octicon octicon-tools"></span> <span class="full-word">Settings</span>
          <img alt="" class="mini-loader" height="16" src="https://assets-cdn.github.com/assets/spinners/octocat-spinner-32-e513294efa576953719e4e2de888dd9cf929b7d62ed8d05f25e731d02452ab6c.gif" width="16" />
</a>      </li>
    </ul>
</nav>

              <div class="only-with-full-nav">
                  
<div class="clone-url open"
  data-protocol-type="http"
  data-url="/users/set_protocol?protocol_selector=http&amp;protocol_type=clone">
  <h3><span class="text-emphasized">HTTPS</span> clone URL</h3>
  <div class="input-group js-zeroclipboard-container">
    <input type="text" class="input-mini input-monospace js-url-field js-zeroclipboard-target"
           value="https://github.com/CCBatIIT/bayesian-itc.git" readonly="readonly">
    <span class="input-group-button">
      <button aria-label="Copy to clipboard" class="js-zeroclipboard btn btn-sm zeroclipboard-button tooltipped tooltipped-s" data-copied-hint="Copied!" data-copy-hint="Copy to clipboard" type="button"><span class="octicon octicon-clippy"></span></button>
    </span>
  </div>
</div>

  
<div class="clone-url "
  data-protocol-type="ssh"
  data-url="/users/set_protocol?protocol_selector=ssh&amp;protocol_type=clone">
  <h3><span class="text-emphasized">SSH</span> clone URL</h3>
  <div class="input-group js-zeroclipboard-container">
    <input type="text" class="input-mini input-monospace js-url-field js-zeroclipboard-target"
           value="git@github.com:CCBatIIT/bayesian-itc.git" readonly="readonly">
    <span class="input-group-button">
      <button aria-label="Copy to clipboard" class="js-zeroclipboard btn btn-sm zeroclipboard-button tooltipped tooltipped-s" data-copied-hint="Copied!" data-copy-hint="Copy to clipboard" type="button"><span class="octicon octicon-clippy"></span></button>
    </span>
  </div>
</div>

  
<div class="clone-url "
  data-protocol-type="subversion"
  data-url="/users/set_protocol?protocol_selector=subversion&amp;protocol_type=clone">
  <h3><span class="text-emphasized">Subversion</span> checkout URL</h3>
  <div class="input-group js-zeroclipboard-container">
    <input type="text" class="input-mini input-monospace js-url-field js-zeroclipboard-target"
           value="https://github.com/CCBatIIT/bayesian-itc" readonly="readonly">
    <span class="input-group-button">
      <button aria-label="Copy to clipboard" class="js-zeroclipboard btn btn-sm zeroclipboard-button tooltipped tooltipped-s" data-copied-hint="Copied!" data-copy-hint="Copy to clipboard" type="button"><span class="octicon octicon-clippy"></span></button>
    </span>
  </div>
</div>



<p class="clone-options">You can clone with
  <a href="#" class="js-clone-selector" data-protocol="http">HTTPS</a>, <a href="#" class="js-clone-selector" data-protocol="ssh">SSH</a>, or <a href="#" class="js-clone-selector" data-protocol="subversion">Subversion</a>.
  <a href="https://help.github.com/articles/which-remote-url-should-i-use" class="help tooltipped tooltipped-n" aria-label="Get help on which URL is right for you.">
    <span class="octicon octicon-question"></span>
  </a>
</p>

  <a href="github-mac://openRepo/https://github.com/CCBatIIT/bayesian-itc" class="btn btn-sm sidebar-button" title="Save CCBatIIT/bayesian-itc to your computer and use it in GitHub Desktop." aria-label="Save CCBatIIT/bayesian-itc to your computer and use it in GitHub Desktop.">
    <span class="octicon octicon-device-desktop"></span>
    Clone in Desktop
  </a>



                <a href="/CCBatIIT/bayesian-itc/archive/racemic_mixture.zip"
                   class="btn btn-sm sidebar-button"
                   aria-label="Download the contents of CCBatIIT/bayesian-itc as a zip file"
                   title="Download the contents of CCBatIIT/bayesian-itc as a zip file"
                   rel="nofollow">
                  <span class="octicon octicon-cloud-download"></span>
                  Download ZIP
                </a>
              </div>
        </div><!-- /.repository-sidebar -->

        <div id="js-repo-pjax-container" class="repository-content context-loader-container" data-pjax-container>
          

<a href="/CCBatIIT/bayesian-itc/blob/ccb9dffb5bc4a04a8b30197033378968f7e2a399/bitc/models.py" class="hidden js-permalink-shortcut" data-hotkey="y">Permalink</a>

<!-- blob contrib key: blob_contributors:v21:e036111af6fb4cf5de9a72cb01e86fa4 -->

<div class="file-navigation js-zeroclipboard-container">
  
<div class="select-menu js-menu-container js-select-menu left">
  <span class="btn btn-sm select-menu-button js-menu-target css-truncate" data-hotkey="w"
    data-master-branch="racemic_mixture"
    data-ref="racemic_mixture"
    title="racemic_mixture"
    role="button" aria-label="Switch branches or tags" tabindex="0" aria-haspopup="true">
    <span class="octicon octicon-git-branch"></span>
    <i>branch:</i>
    <span class="js-select-button css-truncate-target">racemic_mixture</span>
  </span>

  <div class="select-menu-modal-holder js-menu-content js-navigation-container" data-pjax aria-hidden="true">

    <div class="select-menu-modal">
      <div class="select-menu-header">
        <span class="select-menu-title">Switch branches/tags</span>
        <span class="octicon octicon-x js-menu-close" role="button" aria-label="Close"></span>
      </div>

      <div class="select-menu-filters">
        <div class="select-menu-text-filter">
          <input type="text" aria-label="Find or create a branch…" id="context-commitish-filter-field" class="js-filterable-field js-navigation-enable" placeholder="Find or create a branch…">
        </div>
        <div class="select-menu-tabs">
          <ul>
            <li class="select-menu-tab">
              <a href="#" data-tab-filter="branches" data-filter-placeholder="Find or create a branch…" class="js-select-menu-tab">Branches</a>
            </li>
            <li class="select-menu-tab">
              <a href="#" data-tab-filter="tags" data-filter-placeholder="Find a tag…" class="js-select-menu-tab">Tags</a>
            </li>
          </ul>
        </div>
      </div>

      <div class="select-menu-list select-menu-tab-bucket js-select-menu-tab-bucket" data-tab-filter="branches">

        <div data-filterable-for="context-commitish-filter-field" data-filterable-type="substring">


            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/CCBatIIT/bayesian-itc/blob/baseline/bitc/models.py"
               data-name="baseline"
               data-skip-pjax="true"
               rel="nofollow">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <span class="select-menu-item-text css-truncate-target" title="baseline">
                baseline
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/CCBatIIT/bayesian-itc/blob/dmso_water/bitc/models.py"
               data-name="dmso_water"
               data-skip-pjax="true"
               rel="nofollow">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <span class="select-menu-item-text css-truncate-target" title="dmso_water">
                dmso_water
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/CCBatIIT/bayesian-itc/blob/master/bitc/models.py"
               data-name="master"
               data-skip-pjax="true"
               rel="nofollow">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <span class="select-menu-item-text css-truncate-target" title="master">
                master
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open selected"
               href="/CCBatIIT/bayesian-itc/blob/racemic_mixture/bitc/models.py"
               data-name="racemic_mixture"
               data-skip-pjax="true"
               rel="nofollow">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <span class="select-menu-item-text css-truncate-target" title="racemic_mixture">
                racemic_mixture
              </span>
            </a>
        </div>

          <form accept-charset="UTF-8" action="/CCBatIIT/bayesian-itc/branches" class="js-create-branch select-menu-item select-menu-new-item-form js-navigation-item js-new-item-form" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="KSYNYkjM3uPgkr6ppnl9IYfb2oamTzrUrjB0cha5VjddBacnDaiDjpkqa4HDPDj/8nWvQsxJctA3AdWVRZyhhw==" /></div>
            <span class="octicon octicon-git-branch select-menu-item-icon"></span>
            <div class="select-menu-item-text">
              <span class="select-menu-item-heading">Create branch: <span class="js-new-item-name"></span></span>
              <span class="description">from ‘racemic_mixture’</span>
            </div>
            <input type="hidden" name="name" id="name" class="js-new-item-value">
            <input type="hidden" name="branch" id="branch" value="racemic_mixture">
            <input type="hidden" name="path" id="path" value="bitc/models.py">
</form>
      </div>

      <div class="select-menu-list select-menu-tab-bucket js-select-menu-tab-bucket" data-tab-filter="tags">
        <div data-filterable-for="context-commitish-filter-field" data-filterable-type="substring">


        </div>

        <div class="select-menu-no-results">Nothing to show</div>
      </div>

    </div>
  </div>
</div>

  <div class="btn-group right">
    <a href="/CCBatIIT/bayesian-itc/find/racemic_mixture"
          class="js-show-file-finder btn btn-sm empty-icon tooltipped tooltipped-s"
          data-pjax
          data-hotkey="t"
          aria-label="Quickly jump between files">
      <span class="octicon octicon-list-unordered"></span>
    </a>
    <button aria-label="Copy file path to clipboard" class="js-zeroclipboard btn btn-sm zeroclipboard-button tooltipped tooltipped-s" data-copied-hint="Copied!" data-copy-hint="Copy file path to clipboard" type="button"><span class="octicon octicon-clippy"></span></button>
  </div>

  <div class="breadcrumb js-zeroclipboard-target">
    <span class='repo-root js-repo-root'><span itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb"><a href="/CCBatIIT/bayesian-itc" class="" data-branch="racemic_mixture" data-direction="back" data-pjax="true" itemscope="url"><span itemprop="title">bayesian-itc</span></a></span></span><span class="separator">/</span><span itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb"><a href="/CCBatIIT/bayesian-itc/tree/racemic_mixture/bitc" class="" data-branch="racemic_mixture" data-direction="back" data-pjax="true" itemscope="url"><span itemprop="title">bitc</span></a></span><span class="separator">/</span><strong class="final-path">models.py</strong>
  </div>
</div>

<include-fragment class="commit commit-loader file-history-tease" src="/CCBatIIT/bayesian-itc/contributors/racemic_mixture/bitc/models.py">
  <div class="file-history-tease-header">
    Fetching contributors&hellip;
  </div>

  <div class="participation">
    <p class="loader-loading"><img alt="" height="16" src="https://assets-cdn.github.com/assets/spinners/octocat-spinner-32-EAF2F5-0bdc57d34b85c4a4de9d0d1db10cd70e8a95f33ff4f46c5a8c48b4bf4e5a9abe.gif" width="16" /></p>
    <p class="loader-error">Cannot retrieve contributors at this time</p>
  </div>
</include-fragment>
<div class="file">
  <div class="file-header">
    <div class="file-actions">

      <div class="btn-group">
        <a href="/CCBatIIT/bayesian-itc/raw/racemic_mixture/bitc/models.py" class="btn btn-sm " id="raw-url">Raw</a>
          <a href="/CCBatIIT/bayesian-itc/blame/racemic_mixture/bitc/models.py" class="btn btn-sm js-update-url-with-hash">Blame</a>
        <a href="/CCBatIIT/bayesian-itc/commits/racemic_mixture/bitc/models.py" class="btn btn-sm " rel="nofollow">History</a>
      </div>

        <a class="octicon-btn tooltipped tooltipped-nw"
           href="github-mac://openRepo/https://github.com/CCBatIIT/bayesian-itc?branch=racemic_mixture&amp;filepath=bitc%2Fmodels.py"
           aria-label="Open this file in GitHub for Mac">
            <span class="octicon octicon-device-desktop"></span>
        </a>

            <form accept-charset="UTF-8" action="/CCBatIIT/bayesian-itc/edit/racemic_mixture/bitc/models.py" class="inline-form" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="dwb2ubtT1n/JQsWJ59xydLfxf7te2aFUSvaGfiOtqT5ADSadZb7UR66AYmE1ndl2GknMdN0ngvQtYPXladlYLg==" /></div>
              <button class="octicon-btn tooltipped tooltipped-n" type="submit" aria-label="Edit this file" data-hotkey="e" data-disable-with>
                <span class="octicon octicon-pencil"></span>
              </button>
</form>
          <form accept-charset="UTF-8" action="/CCBatIIT/bayesian-itc/delete/racemic_mixture/bitc/models.py" class="inline-form" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="KLETXtbfLYo5GXQ4hiOzP5ulrm5O4Ji/IS16AIdmzfkPFP4Bq5J+/ogUeiq3oibCWr2HKCyNziooS03OI/huJA==" /></div>
            <button class="octicon-btn octicon-btn-danger tooltipped tooltipped-n" type="submit" aria-label="Delete this file" data-disable-with>
              <span class="octicon octicon-trashcan"></span>
            </button>
</form>    </div>

    <div class="file-info">
        912 lines (761 sloc)
        <span class="file-info-divider"></span>
      39.398 kb
    </div>
  </div>
  
  <div class="blob-wrapper data type-python">
      <table class="highlight tab-size-8 js-file-line-container">
      <tr>
        <td id="L1" class="blob-num js-line-number" data-line-number="1"></td>
        <td id="LC1" class="blob-code js-file-line"><span class="pl-c">#!/usr/bin/env python</span></td>
      </tr>
      <tr>
        <td id="L2" class="blob-num js-line-number" data-line-number="2"></td>
        <td id="LC2" class="blob-code js-file-line"><span class="pl-s"><span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L3" class="blob-num js-line-number" data-line-number="3"></td>
        <td id="LC3" class="blob-code js-file-line"><span class="pl-s">PyMC models to describe ITC binding experiments</span></td>
      </tr>
      <tr>
        <td id="L4" class="blob-num js-line-number" data-line-number="4"></td>
        <td id="LC4" class="blob-code js-file-line"><span class="pl-s"><span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L5" class="blob-num js-line-number" data-line-number="5"></td>
        <td id="LC5" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L6" class="blob-num js-line-number" data-line-number="6"></td>
        <td id="LC6" class="blob-code js-file-line"><span class="pl-k">import</span> copy</td>
      </tr>
      <tr>
        <td id="L7" class="blob-num js-line-number" data-line-number="7"></td>
        <td id="LC7" class="blob-code js-file-line"><span class="pl-k">import</span> logging</td>
      </tr>
      <tr>
        <td id="L8" class="blob-num js-line-number" data-line-number="8"></td>
        <td id="LC8" class="blob-code js-file-line"><span class="pl-k">from</span> math <span class="pl-k">import</span> exp, log</td>
      </tr>
      <tr>
        <td id="L9" class="blob-num js-line-number" data-line-number="9"></td>
        <td id="LC9" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L10" class="blob-num js-line-number" data-line-number="10"></td>
        <td id="LC10" class="blob-code js-file-line"><span class="pl-k">import</span> numpy</td>
      </tr>
      <tr>
        <td id="L11" class="blob-num js-line-number" data-line-number="11"></td>
        <td id="LC11" class="blob-code js-file-line"><span class="pl-k">import</span> pymc</td>
      </tr>
      <tr>
        <td id="L12" class="blob-num js-line-number" data-line-number="12"></td>
        <td id="LC12" class="blob-code js-file-line"><span class="pl-k">import</span> scipy.integrate</td>
      </tr>
      <tr>
        <td id="L13" class="blob-num js-line-number" data-line-number="13"></td>
        <td id="LC13" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L14" class="blob-num js-line-number" data-line-number="14"></td>
        <td id="LC14" class="blob-code js-file-line"><span class="pl-k">from</span> bitc.units <span class="pl-k">import</span> ureg, Quantity</td>
      </tr>
      <tr>
        <td id="L15" class="blob-num js-line-number" data-line-number="15"></td>
        <td id="LC15" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L16" class="blob-num js-line-number" data-line-number="16"></td>
        <td id="LC16" class="blob-code js-file-line"><span class="pl-c"># Use module name for logger</span></td>
      </tr>
      <tr>
        <td id="L17" class="blob-num js-line-number" data-line-number="17"></td>
        <td id="LC17" class="blob-code js-file-line">logger <span class="pl-k">=</span> logging.getLogger(<span class="pl-c1">__name__</span>)</td>
      </tr>
      <tr>
        <td id="L18" class="blob-num js-line-number" data-line-number="18"></td>
        <td id="LC18" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L19" class="blob-num js-line-number" data-line-number="19"></td>
        <td id="LC19" class="blob-code js-file-line"><span class="pl-c"># TODO check if rescaling step is still necessary</span></td>
      </tr>
      <tr>
        <td id="L20" class="blob-num js-line-number" data-line-number="20"></td>
        <td id="LC20" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L21" class="blob-num js-line-number" data-line-number="21"></td>
        <td id="LC21" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L22" class="blob-num js-line-number" data-line-number="22"></td>
        <td id="LC22" class="blob-code js-file-line"><span class="pl-k">class</span> <span class="pl-en">RescalingStep</span>(<span class="pl-e">pymc.StepMethod</span>):</td>
      </tr>
      <tr>
        <td id="L23" class="blob-num js-line-number" data-line-number="23"></td>
        <td id="LC23" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L24" class="blob-num js-line-number" data-line-number="24"></td>
        <td id="LC24" class="blob-code js-file-line">    <span class="pl-s"><span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L25" class="blob-num js-line-number" data-line-number="25"></td>
        <td id="LC25" class="blob-code js-file-line"><span class="pl-s">    Rescaling StepMethod for sampling correlated changes in ligand and receptor concentration</span></td>
      </tr>
      <tr>
        <td id="L26" class="blob-num js-line-number" data-line-number="26"></td>
        <td id="LC26" class="blob-code js-file-line"><span class="pl-s">    <span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L27" class="blob-num js-line-number" data-line-number="27"></td>
        <td id="LC27" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L28" class="blob-num js-line-number" data-line-number="28"></td>
        <td id="LC28" class="blob-code js-file-line">    <span class="pl-k">def</span> <span class="pl-en"><span class="pl-c1">__init__</span></span>(<span class="pl-smi">self</span>, <span class="pl-smi">dictionary</span>, <span class="pl-smi">beta</span>, <span class="pl-smi">max_scale</span><span class="pl-k">=</span><span class="pl-c1">1.03</span>, <span class="pl-smi">interval</span><span class="pl-k">=</span><span class="pl-c1">100</span>, <span class="pl-smi">verbose</span><span class="pl-k">=</span><span class="pl-c1">0</span>):</td>
      </tr>
      <tr>
        <td id="L29" class="blob-num js-line-number" data-line-number="29"></td>
        <td id="LC29" class="blob-code js-file-line">        <span class="pl-s"><span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L30" class="blob-num js-line-number" data-line-number="30"></td>
        <td id="LC30" class="blob-code js-file-line"><span class="pl-s">        dictionary (dict) - must contain dictionary of objects for Ls, P0, DeltaH, DeltaG</span></td>
      </tr>
      <tr>
        <td id="L31" class="blob-num js-line-number" data-line-number="31"></td>
        <td id="LC31" class="blob-code js-file-line"><span class="pl-s">        <span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L32" class="blob-num js-line-number" data-line-number="32"></td>
        <td id="LC32" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L33" class="blob-num js-line-number" data-line-number="33"></td>
        <td id="LC33" class="blob-code js-file-line">        <span class="pl-c"># Verbosity flag for pymc</span></td>
      </tr>
      <tr>
        <td id="L34" class="blob-num js-line-number" data-line-number="34"></td>
        <td id="LC34" class="blob-code js-file-line">        <span class="pl-v">self</span>.verbose <span class="pl-k">=</span> verbose</td>
      </tr>
      <tr>
        <td id="L35" class="blob-num js-line-number" data-line-number="35"></td>
        <td id="LC35" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L36" class="blob-num js-line-number" data-line-number="36"></td>
        <td id="LC36" class="blob-code js-file-line">        <span class="pl-c"># Store stochastics.</span></td>
      </tr>
      <tr>
        <td id="L37" class="blob-num js-line-number" data-line-number="37"></td>
        <td id="LC37" class="blob-code js-file-line">        <span class="pl-v">self</span>.dictionary <span class="pl-k">=</span> dictionary</td>
      </tr>
      <tr>
        <td id="L38" class="blob-num js-line-number" data-line-number="38"></td>
        <td id="LC38" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L39" class="blob-num js-line-number" data-line-number="39"></td>
        <td id="LC39" class="blob-code js-file-line">        <span class="pl-c"># Initialize superclass.</span></td>
      </tr>
      <tr>
        <td id="L40" class="blob-num js-line-number" data-line-number="40"></td>
        <td id="LC40" class="blob-code js-file-line">        pymc.StepMethod.<span class="pl-c1">__init__</span>(<span class="pl-v">self</span>, dictionary.values(), verbose)</td>
      </tr>
      <tr>
        <td id="L41" class="blob-num js-line-number" data-line-number="41"></td>
        <td id="LC41" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L42" class="blob-num js-line-number" data-line-number="42"></td>
        <td id="LC42" class="blob-code js-file-line">        <span class="pl-v">self</span>._id <span class="pl-k">=</span> <span class="pl-s"><span class="pl-pds">&#39;</span>RescalingMetropolis_<span class="pl-pds">&#39;</span></span> <span class="pl-k">+</span> <span class="pl-s"><span class="pl-pds">&#39;</span>_<span class="pl-pds">&#39;</span></span>.join([p.<span class="pl-c1">__name__</span> <span class="pl-k">for</span> p <span class="pl-k">in</span> <span class="pl-v">self</span>.stochastics])</td>
      </tr>
      <tr>
        <td id="L43" class="blob-num js-line-number" data-line-number="43"></td>
        <td id="LC43" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L44" class="blob-num js-line-number" data-line-number="44"></td>
        <td id="LC44" class="blob-code js-file-line">        <span class="pl-c"># State variables used to restore the state in a later session.</span></td>
      </tr>
      <tr>
        <td id="L45" class="blob-num js-line-number" data-line-number="45"></td>
        <td id="LC45" class="blob-code js-file-line">        <span class="pl-v">self</span>._state <span class="pl-k">+=</span> [<span class="pl-s"><span class="pl-pds">&#39;</span>max_scale<span class="pl-pds">&#39;</span></span>, <span class="pl-s"><span class="pl-pds">&#39;</span>_current_iter<span class="pl-pds">&#39;</span></span>, <span class="pl-s"><span class="pl-pds">&#39;</span>interval<span class="pl-pds">&#39;</span></span>]</td>
      </tr>
      <tr>
        <td id="L46" class="blob-num js-line-number" data-line-number="46"></td>
        <td id="LC46" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L47" class="blob-num js-line-number" data-line-number="47"></td>
        <td id="LC47" class="blob-code js-file-line">        <span class="pl-v">self</span>.max_scale <span class="pl-k">=</span> max_scale</td>
      </tr>
      <tr>
        <td id="L48" class="blob-num js-line-number" data-line-number="48"></td>
        <td id="LC48" class="blob-code js-file-line">        <span class="pl-v">self</span>.beta <span class="pl-k">=</span> beta</td>
      </tr>
      <tr>
        <td id="L49" class="blob-num js-line-number" data-line-number="49"></td>
        <td id="LC49" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L50" class="blob-num js-line-number" data-line-number="50"></td>
        <td id="LC50" class="blob-code js-file-line">        <span class="pl-v">self</span>._current_iter <span class="pl-k">=</span> <span class="pl-c1">0</span></td>
      </tr>
      <tr>
        <td id="L51" class="blob-num js-line-number" data-line-number="51"></td>
        <td id="LC51" class="blob-code js-file-line">        <span class="pl-v">self</span>.interval <span class="pl-k">=</span> interval</td>
      </tr>
      <tr>
        <td id="L52" class="blob-num js-line-number" data-line-number="52"></td>
        <td id="LC52" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L53" class="blob-num js-line-number" data-line-number="53"></td>
        <td id="LC53" class="blob-code js-file-line">        <span class="pl-v">self</span>.accepted <span class="pl-k">=</span> <span class="pl-c1">0</span></td>
      </tr>
      <tr>
        <td id="L54" class="blob-num js-line-number" data-line-number="54"></td>
        <td id="LC54" class="blob-code js-file-line">        <span class="pl-v">self</span>.rejected <span class="pl-k">=</span> <span class="pl-c1">0</span></td>
      </tr>
      <tr>
        <td id="L55" class="blob-num js-line-number" data-line-number="55"></td>
        <td id="LC55" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L56" class="blob-num js-line-number" data-line-number="56"></td>
        <td id="LC56" class="blob-code js-file-line">        <span class="pl-c"># Report</span></td>
      </tr>
      <tr>
        <td id="L57" class="blob-num js-line-number" data-line-number="57"></td>
        <td id="LC57" class="blob-code js-file-line">        logger.info(<span class="pl-s"><span class="pl-pds">&quot;</span>Initialization...<span class="pl-cce">\n</span><span class="pl-pds">&quot;</span></span> <span class="pl-k">+</span> <span class="pl-s"><span class="pl-pds">&quot;</span>max_scale: <span class="pl-c1">%s</span><span class="pl-pds">&quot;</span></span> <span class="pl-k">%</span> <span class="pl-v">self</span>.max_scale)</td>
      </tr>
      <tr>
        <td id="L58" class="blob-num js-line-number" data-line-number="58"></td>
        <td id="LC58" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L59" class="blob-num js-line-number" data-line-number="59"></td>
        <td id="LC59" class="blob-code js-file-line">    <span class="pl-k">def</span> <span class="pl-en">propose</span>(<span class="pl-smi">self</span>):</td>
      </tr>
      <tr>
        <td id="L60" class="blob-num js-line-number" data-line-number="60"></td>
        <td id="LC60" class="blob-code js-file-line">        <span class="pl-c"># Choose trial scaling factor or its inverse with equal probability, so</span></td>
      </tr>
      <tr>
        <td id="L61" class="blob-num js-line-number" data-line-number="61"></td>
        <td id="LC61" class="blob-code js-file-line">        <span class="pl-c"># that proposal move is symmetric.</span></td>
      </tr>
      <tr>
        <td id="L62" class="blob-num js-line-number" data-line-number="62"></td>
        <td id="LC62" class="blob-code js-file-line">        factor <span class="pl-k">=</span> (<span class="pl-v">self</span>.max_scale <span class="pl-k">-</span> <span class="pl-c1">1</span>) <span class="pl-k">*</span> numpy.random.rand() <span class="pl-k">+</span> <span class="pl-c1">1</span></td>
      </tr>
      <tr>
        <td id="L63" class="blob-num js-line-number" data-line-number="63"></td>
        <td id="LC63" class="blob-code js-file-line">        <span class="pl-k">if</span> numpy.random.rand() <span class="pl-k">&lt;</span> <span class="pl-c1">0.5</span>:</td>
      </tr>
      <tr>
        <td id="L64" class="blob-num js-line-number" data-line-number="64"></td>
        <td id="LC64" class="blob-code js-file-line">            factor <span class="pl-k">=</span> <span class="pl-c1">1.</span> <span class="pl-k">/</span> factor</td>
      </tr>
      <tr>
        <td id="L65" class="blob-num js-line-number" data-line-number="65"></td>
        <td id="LC65" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L66" class="blob-num js-line-number" data-line-number="66"></td>
        <td id="LC66" class="blob-code js-file-line">        <span class="pl-c"># Scale thermodynamic parameters and variables with this factor.</span></td>
      </tr>
      <tr>
        <td id="L67" class="blob-num js-line-number" data-line-number="67"></td>
        <td id="LC67" class="blob-code js-file-line">        <span class="pl-v">self</span>.dictionary[<span class="pl-s"><span class="pl-pds">&#39;</span>Ls<span class="pl-pds">&#39;</span></span>].value <span class="pl-k">=</span> <span class="pl-v">self</span>.dictionary[<span class="pl-s"><span class="pl-pds">&#39;</span>Ls<span class="pl-pds">&#39;</span></span>].value <span class="pl-k">*</span> factor</td>
      </tr>
      <tr>
        <td id="L68" class="blob-num js-line-number" data-line-number="68"></td>
        <td id="LC68" class="blob-code js-file-line">        <span class="pl-v">self</span>.dictionary[<span class="pl-s"><span class="pl-pds">&#39;</span>P0<span class="pl-pds">&#39;</span></span>].value <span class="pl-k">=</span> <span class="pl-v">self</span>.dictionary[<span class="pl-s"><span class="pl-pds">&#39;</span>P0<span class="pl-pds">&#39;</span></span>].value <span class="pl-k">*</span> factor</td>
      </tr>
      <tr>
        <td id="L69" class="blob-num js-line-number" data-line-number="69"></td>
        <td id="LC69" class="blob-code js-file-line">        <span class="pl-v">self</span>.dictionary[<span class="pl-s"><span class="pl-pds">&#39;</span>DeltaH<span class="pl-pds">&#39;</span></span>].value <span class="pl-k">=</span> <span class="pl-v">self</span>.dictionary[<span class="pl-s"><span class="pl-pds">&#39;</span>DeltaH<span class="pl-pds">&#39;</span></span>].value <span class="pl-k">/</span> factor</td>
      </tr>
      <tr>
        <td id="L70" class="blob-num js-line-number" data-line-number="70"></td>
        <td id="LC70" class="blob-code js-file-line">        <span class="pl-c"># calling magnitude seems flaky, where are the units here?</span></td>
      </tr>
      <tr>
        <td id="L71" class="blob-num js-line-number" data-line-number="71"></td>
        <td id="LC71" class="blob-code js-file-line">        <span class="pl-v">self</span>.dictionary[<span class="pl-s"><span class="pl-pds">&#39;</span>DeltaG<span class="pl-pds">&#39;</span></span>].value <span class="pl-k">=</span> <span class="pl-v">self</span>.dictionary[<span class="pl-s"><span class="pl-pds">&#39;</span>DeltaG<span class="pl-pds">&#39;</span></span>].value <span class="pl-k">+</span> (<span class="pl-c1">1.</span> <span class="pl-k">/</span> <span class="pl-v">self</span>.beta.magnitude) <span class="pl-k">*</span> numpy.log(factor)</td>
      </tr>
      <tr>
        <td id="L72" class="blob-num js-line-number" data-line-number="72"></td>
        <td id="LC72" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L73" class="blob-num js-line-number" data-line-number="73"></td>
        <td id="LC73" class="blob-code js-file-line">        <span class="pl-k">return</span></td>
      </tr>
      <tr>
        <td id="L74" class="blob-num js-line-number" data-line-number="74"></td>
        <td id="LC74" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L75" class="blob-num js-line-number" data-line-number="75"></td>
        <td id="LC75" class="blob-code js-file-line">    <span class="pl-k">def</span> <span class="pl-en">step</span>(<span class="pl-smi">self</span>):</td>
      </tr>
      <tr>
        <td id="L76" class="blob-num js-line-number" data-line-number="76"></td>
        <td id="LC76" class="blob-code js-file-line">        <span class="pl-c"># Probability and likelihood for stochastic&#39;s current value:</span></td>
      </tr>
      <tr>
        <td id="L77" class="blob-num js-line-number" data-line-number="77"></td>
        <td id="LC77" class="blob-code js-file-line">        logp <span class="pl-k">=</span> <span class="pl-c1">sum</span>([stochastic.logp <span class="pl-k">for</span> stochastic <span class="pl-k">in</span> <span class="pl-v">self</span>.stochastics])</td>
      </tr>
      <tr>
        <td id="L78" class="blob-num js-line-number" data-line-number="78"></td>
        <td id="LC78" class="blob-code js-file-line">        loglike <span class="pl-k">=</span> <span class="pl-v">self</span>.loglike</td>
      </tr>
      <tr>
        <td id="L79" class="blob-num js-line-number" data-line-number="79"></td>
        <td id="LC79" class="blob-code js-file-line">        logger.info(<span class="pl-s"><span class="pl-pds">&#39;</span>Current likelihood: <span class="pl-c1">%f</span>, <span class="pl-c1">%f</span><span class="pl-pds">&#39;</span></span> <span class="pl-k">%</span> (logp, loglike))</td>
      </tr>
      <tr>
        <td id="L80" class="blob-num js-line-number" data-line-number="80"></td>
        <td id="LC80" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L81" class="blob-num js-line-number" data-line-number="81"></td>
        <td id="LC81" class="blob-code js-file-line">        <span class="pl-c"># Sample a candidate value</span></td>
      </tr>
      <tr>
        <td id="L82" class="blob-num js-line-number" data-line-number="82"></td>
        <td id="LC82" class="blob-code js-file-line">        <span class="pl-v">self</span>.propose()</td>
      </tr>
      <tr>
        <td id="L83" class="blob-num js-line-number" data-line-number="83"></td>
        <td id="LC83" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L84" class="blob-num js-line-number" data-line-number="84"></td>
        <td id="LC84" class="blob-code js-file-line">        <span class="pl-c"># Metropolis acception/rejection test</span></td>
      </tr>
      <tr>
        <td id="L85" class="blob-num js-line-number" data-line-number="85"></td>
        <td id="LC85" class="blob-code js-file-line">        accept <span class="pl-k">=</span> <span class="pl-c1">False</span></td>
      </tr>
      <tr>
        <td id="L86" class="blob-num js-line-number" data-line-number="86"></td>
        <td id="LC86" class="blob-code js-file-line">        <span class="pl-k">try</span>:</td>
      </tr>
      <tr>
        <td id="L87" class="blob-num js-line-number" data-line-number="87"></td>
        <td id="LC87" class="blob-code js-file-line">            <span class="pl-c"># Probability and likelihood for stochastic&#39;s proposed value:</span></td>
      </tr>
      <tr>
        <td id="L88" class="blob-num js-line-number" data-line-number="88"></td>
        <td id="LC88" class="blob-code js-file-line">            logp_p <span class="pl-k">=</span> <span class="pl-c1">sum</span>([stochastic.logp <span class="pl-k">for</span> stochastic <span class="pl-k">in</span> <span class="pl-v">self</span>.stochastics])</td>
      </tr>
      <tr>
        <td id="L89" class="blob-num js-line-number" data-line-number="89"></td>
        <td id="LC89" class="blob-code js-file-line">            loglike_p <span class="pl-k">=</span> <span class="pl-v">self</span>.loglike</td>
      </tr>
      <tr>
        <td id="L90" class="blob-num js-line-number" data-line-number="90"></td>
        <td id="LC90" class="blob-code js-file-line">            logger.debug(<span class="pl-s"><span class="pl-pds">&#39;</span>Current likelihood: <span class="pl-c1">%f</span>, <span class="pl-c1">%f</span> <span class="pl-pds">&#39;</span></span> <span class="pl-k">%</span> (logp, loglike))</td>
      </tr>
      <tr>
        <td id="L91" class="blob-num js-line-number" data-line-number="91"></td>
        <td id="LC91" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L92" class="blob-num js-line-number" data-line-number="92"></td>
        <td id="LC92" class="blob-code js-file-line">            <span class="pl-k">if</span> numpy.log(numpy.random.rand()) <span class="pl-k">&lt;</span> logp_p <span class="pl-k">+</span> loglike_p <span class="pl-k">-</span> logp <span class="pl-k">-</span> loglike:</td>
      </tr>
      <tr>
        <td id="L93" class="blob-num js-line-number" data-line-number="93"></td>
        <td id="LC93" class="blob-code js-file-line">                accept <span class="pl-k">=</span> <span class="pl-c1">True</span></td>
      </tr>
      <tr>
        <td id="L94" class="blob-num js-line-number" data-line-number="94"></td>
        <td id="LC94" class="blob-code js-file-line">                <span class="pl-v">self</span>.accepted <span class="pl-k">+=</span> <span class="pl-c1">1</span></td>
      </tr>
      <tr>
        <td id="L95" class="blob-num js-line-number" data-line-number="95"></td>
        <td id="LC95" class="blob-code js-file-line">                logger.debug(<span class="pl-s"><span class="pl-pds">&#39;</span>Accepted<span class="pl-pds">&#39;</span></span>)</td>
      </tr>
      <tr>
        <td id="L96" class="blob-num js-line-number" data-line-number="96"></td>
        <td id="LC96" class="blob-code js-file-line">            <span class="pl-k">else</span>:</td>
      </tr>
      <tr>
        <td id="L97" class="blob-num js-line-number" data-line-number="97"></td>
        <td id="LC97" class="blob-code js-file-line">                <span class="pl-v">self</span>.rejected <span class="pl-k">+=</span> <span class="pl-c1">1</span></td>
      </tr>
      <tr>
        <td id="L98" class="blob-num js-line-number" data-line-number="98"></td>
        <td id="LC98" class="blob-code js-file-line">                logger.debug(<span class="pl-s"><span class="pl-pds">&#39;</span>Rejected<span class="pl-pds">&#39;</span></span>)</td>
      </tr>
      <tr>
        <td id="L99" class="blob-num js-line-number" data-line-number="99"></td>
        <td id="LC99" class="blob-code js-file-line">        <span class="pl-k">except</span> pymc.ZeroProbability:</td>
      </tr>
      <tr>
        <td id="L100" class="blob-num js-line-number" data-line-number="100"></td>
        <td id="LC100" class="blob-code js-file-line">            <span class="pl-v">self</span>.rejected <span class="pl-k">+=</span> <span class="pl-c1">1</span></td>
      </tr>
      <tr>
        <td id="L101" class="blob-num js-line-number" data-line-number="101"></td>
        <td id="LC101" class="blob-code js-file-line">            logp_p <span class="pl-k">=</span> <span class="pl-c1">None</span></td>
      </tr>
      <tr>
        <td id="L102" class="blob-num js-line-number" data-line-number="102"></td>
        <td id="LC102" class="blob-code js-file-line">            loglike_p <span class="pl-k">=</span> <span class="pl-c1">None</span></td>
      </tr>
      <tr>
        <td id="L103" class="blob-num js-line-number" data-line-number="103"></td>
        <td id="LC103" class="blob-code js-file-line">            logger.debug(<span class="pl-s"><span class="pl-pds">&#39;</span>Rejected with ZeroProbability error.<span class="pl-pds">&#39;</span></span>)</td>
      </tr>
      <tr>
        <td id="L104" class="blob-num js-line-number" data-line-number="104"></td>
        <td id="LC104" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L105" class="blob-num js-line-number" data-line-number="105"></td>
        <td id="LC105" class="blob-code js-file-line">        <span class="pl-k">if</span> <span class="pl-k">not</span> <span class="pl-v">self</span>._current_iter <span class="pl-k">%</span> <span class="pl-v">self</span>.interval:</td>
      </tr>
      <tr>
        <td id="L106" class="blob-num js-line-number" data-line-number="106"></td>
        <td id="LC106" class="blob-code js-file-line">            logger.info(<span class="pl-s"><span class="pl-pds">&quot;</span>Step <span class="pl-c1">%d</span> <span class="pl-cce">\n</span><span class="pl-pds">&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L107" class="blob-num js-line-number" data-line-number="107"></td>
        <td id="LC107" class="blob-code js-file-line">                        <span class="pl-s"><span class="pl-pds">&quot;</span>Logprobability (current, proposed): <span class="pl-c1">%s</span>, <span class="pl-c1">%s</span> <span class="pl-cce">\n</span><span class="pl-pds">&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L108" class="blob-num js-line-number" data-line-number="108"></td>
        <td id="LC108" class="blob-code js-file-line">                        <span class="pl-s"><span class="pl-pds">&quot;</span>loglike (current, proposed):  <span class="pl-c1">%s</span>, <span class="pl-c1">%s</span>    :<span class="pl-pds">&quot;</span></span> <span class="pl-k">%</span> (<span class="pl-v">self</span>._current_iter,</td>
      </tr>
      <tr>
        <td id="L109" class="blob-num js-line-number" data-line-number="109"></td>
        <td id="LC109" class="blob-code js-file-line">                                                                       logp,</td>
      </tr>
      <tr>
        <td id="L110" class="blob-num js-line-number" data-line-number="110"></td>
        <td id="LC110" class="blob-code js-file-line">                                                                       logp_p,</td>
      </tr>
      <tr>
        <td id="L111" class="blob-num js-line-number" data-line-number="111"></td>
        <td id="LC111" class="blob-code js-file-line">                                                                       loglike,</td>
      </tr>
      <tr>
        <td id="L112" class="blob-num js-line-number" data-line-number="112"></td>
        <td id="LC112" class="blob-code js-file-line">                                                                       loglike_p</td>
      </tr>
      <tr>
        <td id="L113" class="blob-num js-line-number" data-line-number="113"></td>
        <td id="LC113" class="blob-code js-file-line">                                                                       )</td>
      </tr>
      <tr>
        <td id="L114" class="blob-num js-line-number" data-line-number="114"></td>
        <td id="LC114" class="blob-code js-file-line">                        )</td>
      </tr>
      <tr>
        <td id="L115" class="blob-num js-line-number" data-line-number="115"></td>
        <td id="LC115" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L116" class="blob-num js-line-number" data-line-number="116"></td>
        <td id="LC116" class="blob-code js-file-line">            <span class="pl-k">for</span> stochastic <span class="pl-k">in</span> <span class="pl-v">self</span>.stochastics:</td>
      </tr>
      <tr>
        <td id="L117" class="blob-num js-line-number" data-line-number="117"></td>
        <td id="LC117" class="blob-code js-file-line">                logger.info(<span class="pl-s"><span class="pl-pds">&quot;</span><span class="pl-cce">\t</span><span class="pl-pds">&quot;</span></span> <span class="pl-k">+</span> <span class="pl-c1">str</span>(stochastic.<span class="pl-c1">__name__</span>) <span class="pl-k">+</span></td>
      </tr>
      <tr>
        <td id="L118" class="blob-num js-line-number" data-line-number="118"></td>
        <td id="LC118" class="blob-code js-file-line">                            <span class="pl-c1">str</span>(stochastic.last_value) <span class="pl-k">+</span> <span class="pl-c1">str</span>(stochastic.value))</td>
      </tr>
      <tr>
        <td id="L119" class="blob-num js-line-number" data-line-number="119"></td>
        <td id="LC119" class="blob-code js-file-line">            <span class="pl-k">if</span> accept:</td>
      </tr>
      <tr>
        <td id="L120" class="blob-num js-line-number" data-line-number="120"></td>
        <td id="LC120" class="blob-code js-file-line">                logger.info(<span class="pl-s"><span class="pl-pds">&quot;</span><span class="pl-cce">\t</span>Accepted<span class="pl-cce">\t</span>*******<span class="pl-cce">\n</span><span class="pl-pds">&quot;</span></span>)</td>
      </tr>
      <tr>
        <td id="L121" class="blob-num js-line-number" data-line-number="121"></td>
        <td id="LC121" class="blob-code js-file-line">            <span class="pl-k">else</span>:</td>
      </tr>
      <tr>
        <td id="L122" class="blob-num js-line-number" data-line-number="122"></td>
        <td id="LC122" class="blob-code js-file-line">                logger.info(<span class="pl-s"><span class="pl-pds">&quot;</span><span class="pl-cce">\t</span>Rejected<span class="pl-cce">\n</span><span class="pl-pds">&quot;</span></span>)</td>
      </tr>
      <tr>
        <td id="L123" class="blob-num js-line-number" data-line-number="123"></td>
        <td id="LC123" class="blob-code js-file-line">            logger.info(</td>
      </tr>
      <tr>
        <td id="L124" class="blob-num js-line-number" data-line-number="124"></td>
        <td id="LC124" class="blob-code js-file-line">                <span class="pl-s"><span class="pl-pds">&quot;</span><span class="pl-cce">\t</span>Acceptance ratio: <span class="pl-pds">&quot;</span></span> <span class="pl-k">+</span> <span class="pl-c1">str</span>(<span class="pl-v">self</span>.accepted <span class="pl-k">/</span> (<span class="pl-v">self</span>.accepted <span class="pl-k">+</span> <span class="pl-v">self</span>.rejected)))</td>
      </tr>
      <tr>
        <td id="L125" class="blob-num js-line-number" data-line-number="125"></td>
        <td id="LC125" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L126" class="blob-num js-line-number" data-line-number="126"></td>
        <td id="LC126" class="blob-code js-file-line">        <span class="pl-k">if</span> <span class="pl-k">not</span> accept:</td>
      </tr>
      <tr>
        <td id="L127" class="blob-num js-line-number" data-line-number="127"></td>
        <td id="LC127" class="blob-code js-file-line">            <span class="pl-v">self</span>.reject()</td>
      </tr>
      <tr>
        <td id="L128" class="blob-num js-line-number" data-line-number="128"></td>
        <td id="LC128" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L129" class="blob-num js-line-number" data-line-number="129"></td>
        <td id="LC129" class="blob-code js-file-line">        <span class="pl-v">self</span>._current_iter <span class="pl-k">+=</span> <span class="pl-c1">1</span></td>
      </tr>
      <tr>
        <td id="L130" class="blob-num js-line-number" data-line-number="130"></td>
        <td id="LC130" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L131" class="blob-num js-line-number" data-line-number="131"></td>
        <td id="LC131" class="blob-code js-file-line">        <span class="pl-k">return</span></td>
      </tr>
      <tr>
        <td id="L132" class="blob-num js-line-number" data-line-number="132"></td>
        <td id="LC132" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L133" class="blob-num js-line-number" data-line-number="133"></td>
        <td id="LC133" class="blob-code js-file-line">    <span class="pl-en">@<span class="pl-c1">classmethod</span></span></td>
      </tr>
      <tr>
        <td id="L134" class="blob-num js-line-number" data-line-number="134"></td>
        <td id="LC134" class="blob-code js-file-line">    <span class="pl-k">def</span> <span class="pl-en">competence</span>(<span class="pl-smi">cls</span>, <span class="pl-smi">stochastic</span>):</td>
      </tr>
      <tr>
        <td id="L135" class="blob-num js-line-number" data-line-number="135"></td>
        <td id="LC135" class="blob-code js-file-line">        <span class="pl-k">if</span> <span class="pl-c1">str</span>(stochastic) <span class="pl-k">in</span> [<span class="pl-s"><span class="pl-pds">&#39;</span>DeltaG<span class="pl-pds">&#39;</span></span>, <span class="pl-s"><span class="pl-pds">&#39;</span>DeltaH<span class="pl-pds">&#39;</span></span>, <span class="pl-s"><span class="pl-pds">&#39;</span>DeltaH_0<span class="pl-pds">&#39;</span></span>, <span class="pl-s"><span class="pl-pds">&#39;</span>Ls<span class="pl-pds">&#39;</span></span>, <span class="pl-s"><span class="pl-pds">&#39;</span>P0<span class="pl-pds">&#39;</span></span>]:</td>
      </tr>
      <tr>
        <td id="L136" class="blob-num js-line-number" data-line-number="136"></td>
        <td id="LC136" class="blob-code js-file-line">            <span class="pl-k">return</span> <span class="pl-c1">1</span></td>
      </tr>
      <tr>
        <td id="L137" class="blob-num js-line-number" data-line-number="137"></td>
        <td id="LC137" class="blob-code js-file-line">        <span class="pl-k">return</span> <span class="pl-c1">0</span></td>
      </tr>
      <tr>
        <td id="L138" class="blob-num js-line-number" data-line-number="138"></td>
        <td id="LC138" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L139" class="blob-num js-line-number" data-line-number="139"></td>
        <td id="LC139" class="blob-code js-file-line">    <span class="pl-k">def</span> <span class="pl-en">reject</span>(<span class="pl-smi">self</span>):</td>
      </tr>
      <tr>
        <td id="L140" class="blob-num js-line-number" data-line-number="140"></td>
        <td id="LC140" class="blob-code js-file-line">        <span class="pl-k">for</span> stochastic <span class="pl-k">in</span> <span class="pl-v">self</span>.stochastics:</td>
      </tr>
      <tr>
        <td id="L141" class="blob-num js-line-number" data-line-number="141"></td>
        <td id="LC141" class="blob-code js-file-line">            <span class="pl-c"># stochastic.value = stochastic.last_value</span></td>
      </tr>
      <tr>
        <td id="L142" class="blob-num js-line-number" data-line-number="142"></td>
        <td id="LC142" class="blob-code js-file-line">            stochastic.revert()</td>
      </tr>
      <tr>
        <td id="L143" class="blob-num js-line-number" data-line-number="143"></td>
        <td id="LC143" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L144" class="blob-num js-line-number" data-line-number="144"></td>
        <td id="LC144" class="blob-code js-file-line">    <span class="pl-en">@<span class="pl-c1">staticmethod</span></span></td>
      </tr>
      <tr>
        <td id="L145" class="blob-num js-line-number" data-line-number="145"></td>
        <td id="LC145" class="blob-code js-file-line">    <span class="pl-k">def</span> <span class="pl-en">tune</span>(<span class="pl-smi">verbose</span>):</td>
      </tr>
      <tr>
        <td id="L146" class="blob-num js-line-number" data-line-number="146"></td>
        <td id="LC146" class="blob-code js-file-line">        <span class="pl-k">return</span> <span class="pl-c1">False</span></td>
      </tr>
      <tr>
        <td id="L147" class="blob-num js-line-number" data-line-number="147"></td>
        <td id="LC147" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L148" class="blob-num js-line-number" data-line-number="148"></td>
        <td id="LC148" class="blob-code js-file-line"><span class="pl-c"># TODO Move generation of the pymc sampler into a method in this base</span></td>
      </tr>
      <tr>
        <td id="L149" class="blob-num js-line-number" data-line-number="149"></td>
        <td id="LC149" class="blob-code js-file-line"><span class="pl-c"># class: createSampler()?</span></td>
      </tr>
      <tr>
        <td id="L150" class="blob-num js-line-number" data-line-number="150"></td>
        <td id="LC150" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L151" class="blob-num js-line-number" data-line-number="151"></td>
        <td id="LC151" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L152" class="blob-num js-line-number" data-line-number="152"></td>
        <td id="LC152" class="blob-code js-file-line"><span class="pl-k">class</span> <span class="pl-en">BindingModel</span>(<span class="pl-e"><span class="pl-c1">object</span></span>):</td>
      </tr>
      <tr>
        <td id="L153" class="blob-num js-line-number" data-line-number="153"></td>
        <td id="LC153" class="blob-code js-file-line">    <span class="pl-s"><span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L154" class="blob-num js-line-number" data-line-number="154"></td>
        <td id="LC154" class="blob-code js-file-line"><span class="pl-s">    Abstract base class for reaction models.</span></td>
      </tr>
      <tr>
        <td id="L155" class="blob-num js-line-number" data-line-number="155"></td>
        <td id="LC155" class="blob-code js-file-line"><span class="pl-s">    <span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L156" class="blob-num js-line-number" data-line-number="156"></td>
        <td id="LC156" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L157" class="blob-num js-line-number" data-line-number="157"></td>
        <td id="LC157" class="blob-code js-file-line">    <span class="pl-k">def</span> <span class="pl-en"><span class="pl-c1">__init__</span></span>(<span class="pl-smi">self</span>):</td>
      </tr>
      <tr>
        <td id="L158" class="blob-num js-line-number" data-line-number="158"></td>
        <td id="LC158" class="blob-code js-file-line">        <span class="pl-k">pass</span></td>
      </tr>
      <tr>
        <td id="L159" class="blob-num js-line-number" data-line-number="159"></td>
        <td id="LC159" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L160" class="blob-num js-line-number" data-line-number="160"></td>
        <td id="LC160" class="blob-code js-file-line">    <span class="pl-en">@<span class="pl-c1">staticmethod</span></span></td>
      </tr>
      <tr>
        <td id="L161" class="blob-num js-line-number" data-line-number="161"></td>
        <td id="LC161" class="blob-code js-file-line">    <span class="pl-k">def</span> <span class="pl-en">_add_unit_to_guesses</span>(<span class="pl-smi">value</span>, <span class="pl-smi">maximum</span>, <span class="pl-smi">minimum</span>, <span class="pl-smi">unit</span>):</td>
      </tr>
      <tr>
        <td id="L162" class="blob-num js-line-number" data-line-number="162"></td>
        <td id="LC162" class="blob-code js-file-line">        <span class="pl-s"><span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L163" class="blob-num js-line-number" data-line-number="163"></td>
        <td id="LC163" class="blob-code js-file-line"><span class="pl-s">        Add units to inital guesses for priors</span></td>
      </tr>
      <tr>
        <td id="L164" class="blob-num js-line-number" data-line-number="164"></td>
        <td id="LC164" class="blob-code js-file-line"><span class="pl-s">        :param value: mean value of the guess</span></td>
      </tr>
      <tr>
        <td id="L165" class="blob-num js-line-number" data-line-number="165"></td>
        <td id="LC165" class="blob-code js-file-line"><span class="pl-s">        :type value: float</span></td>
      </tr>
      <tr>
        <td id="L166" class="blob-num js-line-number" data-line-number="166"></td>
        <td id="LC166" class="blob-code js-file-line"><span class="pl-s">        :param maximum: maximum for the guess</span></td>
      </tr>
      <tr>
        <td id="L167" class="blob-num js-line-number" data-line-number="167"></td>
        <td id="LC167" class="blob-code js-file-line"><span class="pl-s">        :type maximum: float</span></td>
      </tr>
      <tr>
        <td id="L168" class="blob-num js-line-number" data-line-number="168"></td>
        <td id="LC168" class="blob-code js-file-line"><span class="pl-s">        :param minimum: minimum value of the guess</span></td>
      </tr>
      <tr>
        <td id="L169" class="blob-num js-line-number" data-line-number="169"></td>
        <td id="LC169" class="blob-code js-file-line"><span class="pl-s">        :type minimum: float</span></td>
      </tr>
      <tr>
        <td id="L170" class="blob-num js-line-number" data-line-number="170"></td>
        <td id="LC170" class="blob-code js-file-line"><span class="pl-s">        :param unit: unit to add to the supplied numbers</span></td>
      </tr>
      <tr>
        <td id="L171" class="blob-num js-line-number" data-line-number="171"></td>
        <td id="LC171" class="blob-code js-file-line"><span class="pl-s">        :type unit: Quantity</span></td>
      </tr>
      <tr>
        <td id="L172" class="blob-num js-line-number" data-line-number="172"></td>
        <td id="LC172" class="blob-code js-file-line"><span class="pl-s">        :return: value, maximum and minimum, with units added</span></td>
      </tr>
      <tr>
        <td id="L173" class="blob-num js-line-number" data-line-number="173"></td>
        <td id="LC173" class="blob-code js-file-line"><span class="pl-s">        :rtype: (Quantity,Quantity,Quantity)</span></td>
      </tr>
      <tr>
        <td id="L174" class="blob-num js-line-number" data-line-number="174"></td>
        <td id="LC174" class="blob-code js-file-line"><span class="pl-s">        <span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L175" class="blob-num js-line-number" data-line-number="175"></td>
        <td id="LC175" class="blob-code js-file-line">        value <span class="pl-k">*=</span> unit</td>
      </tr>
      <tr>
        <td id="L176" class="blob-num js-line-number" data-line-number="176"></td>
        <td id="LC176" class="blob-code js-file-line">        maximum <span class="pl-k">*=</span> unit</td>
      </tr>
      <tr>
        <td id="L177" class="blob-num js-line-number" data-line-number="177"></td>
        <td id="LC177" class="blob-code js-file-line">        minimum <span class="pl-k">*=</span> unit</td>
      </tr>
      <tr>
        <td id="L178" class="blob-num js-line-number" data-line-number="178"></td>
        <td id="LC178" class="blob-code js-file-line">        <span class="pl-k">return</span> value, maximum, minimum</td>
      </tr>
      <tr>
        <td id="L179" class="blob-num js-line-number" data-line-number="179"></td>
        <td id="LC179" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L180" class="blob-num js-line-number" data-line-number="180"></td>
        <td id="LC180" class="blob-code js-file-line">    <span class="pl-en">@<span class="pl-c1">staticmethod</span></span></td>
      </tr>
      <tr>
        <td id="L181" class="blob-num js-line-number" data-line-number="181"></td>
        <td id="LC181" class="blob-code js-file-line">    <span class="pl-k">def</span> <span class="pl-en">_deltaH0_guesses</span>(<span class="pl-smi">q_n</span>):</td>
      </tr>
      <tr>
        <td id="L182" class="blob-num js-line-number" data-line-number="182"></td>
        <td id="LC182" class="blob-code js-file-line">        <span class="pl-s"><span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L183" class="blob-num js-line-number" data-line-number="183"></td>
        <td id="LC183" class="blob-code js-file-line"><span class="pl-s">        Provide guesses for deltaH_0 from the last injection in the list of injection heats</span></td>
      </tr>
      <tr>
        <td id="L184" class="blob-num js-line-number" data-line-number="184"></td>
        <td id="LC184" class="blob-code js-file-line"><span class="pl-s">        <span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L185" class="blob-num js-line-number" data-line-number="185"></td>
        <td id="LC185" class="blob-code js-file-line">        <span class="pl-c"># Assume the last injection has the best guess for H0</span></td>
      </tr>
      <tr>
        <td id="L186" class="blob-num js-line-number" data-line-number="186"></td>
        <td id="LC186" class="blob-code js-file-line">        DeltaH_0_guess <span class="pl-k">=</span> q_n[<span class="pl-k">-</span><span class="pl-c1">1</span>]</td>
      </tr>
      <tr>
        <td id="L187" class="blob-num js-line-number" data-line-number="187"></td>
        <td id="LC187" class="blob-code js-file-line">        heat_interval <span class="pl-k">=</span> (q_n.max() <span class="pl-k">-</span> q_n.min())</td>
      </tr>
      <tr>
        <td id="L188" class="blob-num js-line-number" data-line-number="188"></td>
        <td id="LC188" class="blob-code js-file-line">        DeltaH_0_min <span class="pl-k">=</span> q_n.min() <span class="pl-k">-</span> heat_interval</td>
      </tr>
      <tr>
        <td id="L189" class="blob-num js-line-number" data-line-number="189"></td>
        <td id="LC189" class="blob-code js-file-line">        DeltaH_0_max <span class="pl-k">=</span> q_n.max() <span class="pl-k">+</span> heat_interval</td>
      </tr>
      <tr>
        <td id="L190" class="blob-num js-line-number" data-line-number="190"></td>
        <td id="LC190" class="blob-code js-file-line">        <span class="pl-k">return</span> DeltaH_0_guess, DeltaH_0_max, DeltaH_0_min</td>
      </tr>
      <tr>
        <td id="L191" class="blob-num js-line-number" data-line-number="191"></td>
        <td id="LC191" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L192" class="blob-num js-line-number" data-line-number="192"></td>
        <td id="LC192" class="blob-code js-file-line">    <span class="pl-en">@<span class="pl-c1">staticmethod</span></span></td>
      </tr>
      <tr>
        <td id="L193" class="blob-num js-line-number" data-line-number="193"></td>
        <td id="LC193" class="blob-code js-file-line">    <span class="pl-k">def</span> <span class="pl-en">_get_syringe_concentration</span>(<span class="pl-smi">experiment</span>):</td>
      </tr>
      <tr>
        <td id="L194" class="blob-num js-line-number" data-line-number="194"></td>
        <td id="LC194" class="blob-code js-file-line">        <span class="pl-s"><span class="pl-pds">&quot;&quot;&quot;</span>Return the syringe concentration from an experiment</span></td>
      </tr>
      <tr>
        <td id="L195" class="blob-num js-line-number" data-line-number="195"></td>
        <td id="LC195" class="blob-code js-file-line"><span class="pl-s">           for python 2/3 compatibility</span></td>
      </tr>
      <tr>
        <td id="L196" class="blob-num js-line-number" data-line-number="196"></td>
        <td id="LC196" class="blob-code js-file-line"><span class="pl-s">        <span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L197" class="blob-num js-line-number" data-line-number="197"></td>
        <td id="LC197" class="blob-code js-file-line">        <span class="pl-k">try</span>:</td>
      </tr>
      <tr>
        <td id="L198" class="blob-num js-line-number" data-line-number="198"></td>
        <td id="LC198" class="blob-code js-file-line">            Ls_stated <span class="pl-k">=</span> experiment.syringe_concentration.itervalues().next()</td>
      </tr>
      <tr>
        <td id="L199" class="blob-num js-line-number" data-line-number="199"></td>
        <td id="LC199" class="blob-code js-file-line">        <span class="pl-k">except</span> <span class="pl-c1">AttributeError</span>:</td>
      </tr>
      <tr>
        <td id="L200" class="blob-num js-line-number" data-line-number="200"></td>
        <td id="LC200" class="blob-code js-file-line">            Ls_stated <span class="pl-k">=</span> <span class="pl-c1">next</span>(<span class="pl-c1">iter</span>(experiment.syringe_concentration.values()))</td>
      </tr>
      <tr>
        <td id="L201" class="blob-num js-line-number" data-line-number="201"></td>
        <td id="LC201" class="blob-code js-file-line">        <span class="pl-k">return</span> Ls_stated</td>
      </tr>
      <tr>
        <td id="L202" class="blob-num js-line-number" data-line-number="202"></td>
        <td id="LC202" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L203" class="blob-num js-line-number" data-line-number="203"></td>
        <td id="LC203" class="blob-code js-file-line">    <span class="pl-en">@<span class="pl-c1">staticmethod</span></span></td>
      </tr>
      <tr>
        <td id="L204" class="blob-num js-line-number" data-line-number="204"></td>
        <td id="LC204" class="blob-code js-file-line">    <span class="pl-k">def</span> <span class="pl-en">_get_cell_concentration</span>(<span class="pl-smi">experiment</span>):</td>
      </tr>
      <tr>
        <td id="L205" class="blob-num js-line-number" data-line-number="205"></td>
        <td id="LC205" class="blob-code js-file-line">        <span class="pl-s"><span class="pl-pds">&quot;&quot;&quot;</span>Return the cell concentration from an experiment</span></td>
      </tr>
      <tr>
        <td id="L206" class="blob-num js-line-number" data-line-number="206"></td>
        <td id="LC206" class="blob-code js-file-line"><span class="pl-s">            for python 2/3 compatibility</span></td>
      </tr>
      <tr>
        <td id="L207" class="blob-num js-line-number" data-line-number="207"></td>
        <td id="LC207" class="blob-code js-file-line"><span class="pl-s">        <span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L208" class="blob-num js-line-number" data-line-number="208"></td>
        <td id="LC208" class="blob-code js-file-line">        <span class="pl-k">try</span>:</td>
      </tr>
      <tr>
        <td id="L209" class="blob-num js-line-number" data-line-number="209"></td>
        <td id="LC209" class="blob-code js-file-line">            P0_stated <span class="pl-k">=</span> experiment.cell_concentration.itervalues().next()</td>
      </tr>
      <tr>
        <td id="L210" class="blob-num js-line-number" data-line-number="210"></td>
        <td id="LC210" class="blob-code js-file-line">        <span class="pl-k">except</span> <span class="pl-c1">AttributeError</span>:</td>
      </tr>
      <tr>
        <td id="L211" class="blob-num js-line-number" data-line-number="211"></td>
        <td id="LC211" class="blob-code js-file-line">            P0_stated <span class="pl-k">=</span> <span class="pl-c1">next</span>(<span class="pl-c1">iter</span>(experiment.cell_concentration.values()))</td>
      </tr>
      <tr>
        <td id="L212" class="blob-num js-line-number" data-line-number="212"></td>
        <td id="LC212" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L213" class="blob-num js-line-number" data-line-number="213"></td>
        <td id="LC213" class="blob-code js-file-line">        <span class="pl-k">return</span> P0_stated</td>
      </tr>
      <tr>
        <td id="L214" class="blob-num js-line-number" data-line-number="214"></td>
        <td id="LC214" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L215" class="blob-num js-line-number" data-line-number="215"></td>
        <td id="LC215" class="blob-code js-file-line">    <span class="pl-en">@<span class="pl-c1">staticmethod</span></span></td>
      </tr>
      <tr>
        <td id="L216" class="blob-num js-line-number" data-line-number="216"></td>
        <td id="LC216" class="blob-code js-file-line">    <span class="pl-k">def</span> <span class="pl-en">_lognormal_concentration_prior</span>(<span class="pl-smi">name</span>, <span class="pl-smi">stated_concentration</span>, <span class="pl-smi">uncertainty</span>, <span class="pl-smi">unit</span>):</td>
      </tr>
      <tr>
        <td id="L217" class="blob-num js-line-number" data-line-number="217"></td>
        <td id="LC217" class="blob-code js-file-line">        <span class="pl-s"><span class="pl-pds">&quot;&quot;&quot;</span>Define a pymc prior for a concentration, using micromolar units</span></td>
      </tr>
      <tr>
        <td id="L218" class="blob-num js-line-number" data-line-number="218"></td>
        <td id="LC218" class="blob-code js-file-line"><span class="pl-s">        :rtype : pymc.Lognormal</span></td>
      </tr>
      <tr>
        <td id="L219" class="blob-num js-line-number" data-line-number="219"></td>
        <td id="LC219" class="blob-code js-file-line"><span class="pl-s">        <span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L220" class="blob-num js-line-number" data-line-number="220"></td>
        <td id="LC220" class="blob-code js-file-line">        <span class="pl-k">return</span> pymc.Lognormal(name,</td>
      </tr>
      <tr>
        <td id="L221" class="blob-num js-line-number" data-line-number="221"></td>
        <td id="LC221" class="blob-code js-file-line">                              <span class="pl-smi">mu</span><span class="pl-k">=</span>log(stated_concentration <span class="pl-k">/</span> unit),</td>
      </tr>
      <tr>
        <td id="L222" class="blob-num js-line-number" data-line-number="222"></td>
        <td id="LC222" class="blob-code js-file-line">                              <span class="pl-smi">tau</span><span class="pl-k">=</span><span class="pl-c1">1.0</span> <span class="pl-k">/</span> log(<span class="pl-c1">1.0</span> <span class="pl-k">+</span> (uncertainty <span class="pl-k">/</span> stated_concentration) <span class="pl-k">**</span> <span class="pl-c1">2</span>),</td>
      </tr>
      <tr>
        <td id="L223" class="blob-num js-line-number" data-line-number="223"></td>
        <td id="LC223" class="blob-code js-file-line">                              <span class="pl-smi">value</span><span class="pl-k">=</span>stated_concentration <span class="pl-k">/</span> unit</td>
      </tr>
      <tr>
        <td id="L224" class="blob-num js-line-number" data-line-number="224"></td>
        <td id="LC224" class="blob-code js-file-line">        )</td>
      </tr>
      <tr>
        <td id="L225" class="blob-num js-line-number" data-line-number="225"></td>
        <td id="LC225" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L226" class="blob-num js-line-number" data-line-number="226"></td>
        <td id="LC226" class="blob-code js-file-line">    <span class="pl-en">@<span class="pl-c1">staticmethod</span></span></td>
      </tr>
      <tr>
        <td id="L227" class="blob-num js-line-number" data-line-number="227"></td>
        <td id="LC227" class="blob-code js-file-line">    <span class="pl-k">def</span> <span class="pl-en">_normal_observation_with_units</span>(<span class="pl-smi">name</span>, <span class="pl-smi">q_n_model</span>, <span class="pl-smi">q_ns</span>, <span class="pl-smi">tau</span>, <span class="pl-smi">unit</span>):</td>
      </tr>
      <tr>
        <td id="L228" class="blob-num js-line-number" data-line-number="228"></td>
        <td id="LC228" class="blob-code js-file-line">        <span class="pl-s"><span class="pl-pds">&quot;&quot;&quot;</span>Define a set of normally distributed observations, while stripping units</span></td>
      </tr>
      <tr>
        <td id="L229" class="blob-num js-line-number" data-line-number="229"></td>
        <td id="LC229" class="blob-code js-file-line"><span class="pl-s">        :rtype : pymc.Normal</span></td>
      </tr>
      <tr>
        <td id="L230" class="blob-num js-line-number" data-line-number="230"></td>
        <td id="LC230" class="blob-code js-file-line"><span class="pl-s">        <span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L231" class="blob-num js-line-number" data-line-number="231"></td>
        <td id="LC231" class="blob-code js-file-line">        <span class="pl-k">return</span> pymc.Normal(name, <span class="pl-smi">mu</span><span class="pl-k">=</span>q_n_model, <span class="pl-smi">tau</span><span class="pl-k">=</span>tau, <span class="pl-smi">observed</span><span class="pl-k">=</span><span class="pl-c1">True</span>, <span class="pl-smi">value</span><span class="pl-k">=</span>q_ns <span class="pl-k">/</span> unit)</td>
      </tr>
      <tr>
        <td id="L232" class="blob-num js-line-number" data-line-number="232"></td>
        <td id="LC232" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L233" class="blob-num js-line-number" data-line-number="233"></td>
        <td id="LC233" class="blob-code js-file-line">    <span class="pl-en">@<span class="pl-c1">staticmethod</span></span></td>
      </tr>
      <tr>
        <td id="L234" class="blob-num js-line-number" data-line-number="234"></td>
        <td id="LC234" class="blob-code js-file-line">    <span class="pl-k">def</span> <span class="pl-en">_uniform_prior</span>(<span class="pl-smi">name</span>, <span class="pl-smi">value</span>, <span class="pl-smi">maximum</span>, <span class="pl-smi">minimum</span>):</td>
      </tr>
      <tr>
        <td id="L235" class="blob-num js-line-number" data-line-number="235"></td>
        <td id="LC235" class="blob-code js-file-line">        <span class="pl-s"><span class="pl-pds">&quot;&quot;&quot;</span>Define a uniform prior without units</span></td>
      </tr>
      <tr>
        <td id="L236" class="blob-num js-line-number" data-line-number="236"></td>
        <td id="LC236" class="blob-code js-file-line"><span class="pl-s">           Added for consistency with other Bindingmodel</span></td>
      </tr>
      <tr>
        <td id="L237" class="blob-num js-line-number" data-line-number="237"></td>
        <td id="LC237" class="blob-code js-file-line"><span class="pl-s">        :rtype : pymc.Uniform</span></td>
      </tr>
      <tr>
        <td id="L238" class="blob-num js-line-number" data-line-number="238"></td>
        <td id="LC238" class="blob-code js-file-line"><span class="pl-s">        <span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L239" class="blob-num js-line-number" data-line-number="239"></td>
        <td id="LC239" class="blob-code js-file-line">        <span class="pl-k">return</span> pymc.Uniform(name,</td>
      </tr>
      <tr>
        <td id="L240" class="blob-num js-line-number" data-line-number="240"></td>
        <td id="LC240" class="blob-code js-file-line">                            <span class="pl-smi">lower</span><span class="pl-k">=</span>minimum,</td>
      </tr>
      <tr>
        <td id="L241" class="blob-num js-line-number" data-line-number="241"></td>
        <td id="LC241" class="blob-code js-file-line">                            <span class="pl-smi">upper</span><span class="pl-k">=</span>maximum,</td>
      </tr>
      <tr>
        <td id="L242" class="blob-num js-line-number" data-line-number="242"></td>
        <td id="LC242" class="blob-code js-file-line">                            <span class="pl-smi">value</span><span class="pl-k">=</span>value</td>
      </tr>
      <tr>
        <td id="L243" class="blob-num js-line-number" data-line-number="243"></td>
        <td id="LC243" class="blob-code js-file-line">        )</td>
      </tr>
      <tr>
        <td id="L244" class="blob-num js-line-number" data-line-number="244"></td>
        <td id="LC244" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L245" class="blob-num js-line-number" data-line-number="245"></td>
        <td id="LC245" class="blob-code js-file-line">    <span class="pl-en">@<span class="pl-c1">staticmethod</span></span></td>
      </tr>
      <tr>
        <td id="L246" class="blob-num js-line-number" data-line-number="246"></td>
        <td id="LC246" class="blob-code js-file-line">    <span class="pl-k">def</span> <span class="pl-en">_uniform_prior_with_units</span>(<span class="pl-smi">name</span>, <span class="pl-smi">value</span>, <span class="pl-smi">maximum</span>, <span class="pl-smi">minimum</span>, <span class="pl-smi">unit</span>):</td>
      </tr>
      <tr>
        <td id="L247" class="blob-num js-line-number" data-line-number="247"></td>
        <td id="LC247" class="blob-code js-file-line">        <span class="pl-s"><span class="pl-pds">&quot;&quot;&quot;</span>Define a uniform prior, while stripping units</span></td>
      </tr>
      <tr>
        <td id="L248" class="blob-num js-line-number" data-line-number="248"></td>
        <td id="LC248" class="blob-code js-file-line"><span class="pl-s">        :rtype : pymc.Uniform</span></td>
      </tr>
      <tr>
        <td id="L249" class="blob-num js-line-number" data-line-number="249"></td>
        <td id="LC249" class="blob-code js-file-line"><span class="pl-s">        <span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L250" class="blob-num js-line-number" data-line-number="250"></td>
        <td id="LC250" class="blob-code js-file-line">        <span class="pl-k">return</span> pymc.Uniform(name,</td>
      </tr>
      <tr>
        <td id="L251" class="blob-num js-line-number" data-line-number="251"></td>
        <td id="LC251" class="blob-code js-file-line">                            <span class="pl-smi">lower</span><span class="pl-k">=</span>minimum <span class="pl-k">/</span> unit,</td>
      </tr>
      <tr>
        <td id="L252" class="blob-num js-line-number" data-line-number="252"></td>
        <td id="LC252" class="blob-code js-file-line">                            <span class="pl-smi">upper</span><span class="pl-k">=</span>maximum <span class="pl-k">/</span> unit,</td>
      </tr>
      <tr>
        <td id="L253" class="blob-num js-line-number" data-line-number="253"></td>
        <td id="LC253" class="blob-code js-file-line">                            <span class="pl-smi">value</span><span class="pl-k">=</span>value <span class="pl-k">/</span> unit</td>
      </tr>
      <tr>
        <td id="L254" class="blob-num js-line-number" data-line-number="254"></td>
        <td id="LC254" class="blob-code js-file-line">        )</td>
      </tr>
      <tr>
        <td id="L255" class="blob-num js-line-number" data-line-number="255"></td>
        <td id="LC255" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L256" class="blob-num js-line-number" data-line-number="256"></td>
        <td id="LC256" class="blob-code js-file-line">    <span class="pl-en">@<span class="pl-c1">staticmethod</span></span></td>
      </tr>
      <tr>
        <td id="L257" class="blob-num js-line-number" data-line-number="257"></td>
        <td id="LC257" class="blob-code js-file-line">    <span class="pl-k">def</span> <span class="pl-en">_uniform_prior_with_guesses_and_units</span>(<span class="pl-smi">name</span>, <span class="pl-smi">value</span>, <span class="pl-smi">maximum</span>, <span class="pl-smi">minimum</span>, <span class="pl-smi">prior_unit</span>, <span class="pl-smi">guess_unit</span><span class="pl-k">=</span><span class="pl-c1">None</span>):</td>
      </tr>
      <tr>
        <td id="L258" class="blob-num js-line-number" data-line-number="258"></td>
        <td id="LC258" class="blob-code js-file-line">        <span class="pl-s"><span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L259" class="blob-num js-line-number" data-line-number="259"></td>
        <td id="LC259" class="blob-code js-file-line"><span class="pl-s">        Take initial values, add units or convert units to the right type,</span></td>
      </tr>
      <tr>
        <td id="L260" class="blob-num js-line-number" data-line-number="260"></td>
        <td id="LC260" class="blob-code js-file-line"><span class="pl-s">        returns a pymc uniform prior</span></td>
      </tr>
      <tr>
        <td id="L261" class="blob-num js-line-number" data-line-number="261"></td>
        <td id="LC261" class="blob-code js-file-line"><span class="pl-s">        :rtype : pymc.Uniform</span></td>
      </tr>
      <tr>
        <td id="L262" class="blob-num js-line-number" data-line-number="262"></td>
        <td id="LC262" class="blob-code js-file-line"><span class="pl-s">        <span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L263" class="blob-num js-line-number" data-line-number="263"></td>
        <td id="LC263" class="blob-code js-file-line">        <span class="pl-c"># Guess has units</span></td>
      </tr>
      <tr>
        <td id="L264" class="blob-num js-line-number" data-line-number="264"></td>
        <td id="LC264" class="blob-code js-file-line">        <span class="pl-k">if</span> guess_unit <span class="pl-k">is</span> <span class="pl-c1">True</span>:</td>
      </tr>
      <tr>
        <td id="L265" class="blob-num js-line-number" data-line-number="265"></td>
        <td id="LC265" class="blob-code js-file-line">            <span class="pl-k">pass</span></td>
      </tr>
      <tr>
        <td id="L266" class="blob-num js-line-number" data-line-number="266"></td>
        <td id="LC266" class="blob-code js-file-line">        <span class="pl-c"># guess provided has no units, but should be same as prior</span></td>
      </tr>
      <tr>
        <td id="L267" class="blob-num js-line-number" data-line-number="267"></td>
        <td id="LC267" class="blob-code js-file-line">        <span class="pl-k">elif</span> guess_unit <span class="pl-k">in</span> {<span class="pl-c1">None</span>, <span class="pl-c1">False</span>}:</td>
      </tr>
      <tr>
        <td id="L268" class="blob-num js-line-number" data-line-number="268"></td>
        <td id="LC268" class="blob-code js-file-line">            guess_unit <span class="pl-k">=</span> prior_unit</td>
      </tr>
      <tr>
        <td id="L269" class="blob-num js-line-number" data-line-number="269"></td>
        <td id="LC269" class="blob-code js-file-line">            value, maximum, minimum <span class="pl-k">=</span> BindingModel._add_unit_to_guesses(value, maximum, minimum, guess_unit)</td>
      </tr>
      <tr>
        <td id="L270" class="blob-num js-line-number" data-line-number="270"></td>
        <td id="LC270" class="blob-code js-file-line">        <span class="pl-c"># guess unit is a unit and needs to be assigned to the guesses first</span></td>
      </tr>
      <tr>
        <td id="L271" class="blob-num js-line-number" data-line-number="271"></td>
        <td id="LC271" class="blob-code js-file-line">        <span class="pl-k">else</span>:</td>
      </tr>
      <tr>
        <td id="L272" class="blob-num js-line-number" data-line-number="272"></td>
        <td id="LC272" class="blob-code js-file-line">            value, maximum, minimum <span class="pl-k">=</span> BindingModel._add_unit_to_guesses(value, maximum, minimum, guess_unit)</td>
      </tr>
      <tr>
        <td id="L273" class="blob-num js-line-number" data-line-number="273"></td>
        <td id="LC273" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L274" class="blob-num js-line-number" data-line-number="274"></td>
        <td id="LC274" class="blob-code js-file-line">        <span class="pl-k">return</span> BindingModel._uniform_prior_with_units(name, value, maximum, minimum, prior_unit)</td>
      </tr>
      <tr>
        <td id="L275" class="blob-num js-line-number" data-line-number="275"></td>
        <td id="LC275" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L276" class="blob-num js-line-number" data-line-number="276"></td>
        <td id="LC276" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L277" class="blob-num js-line-number" data-line-number="277"></td>
        <td id="LC277" class="blob-code js-file-line"><span class="pl-k">class</span> <span class="pl-en">TwoComponentBindingModel</span>(<span class="pl-e">BindingModel</span>):</td>
      </tr>
      <tr>
        <td id="L278" class="blob-num js-line-number" data-line-number="278"></td>
        <td id="LC278" class="blob-code js-file-line">    <span class="pl-s"><span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L279" class="blob-num js-line-number" data-line-number="279"></td>
        <td id="LC279" class="blob-code js-file-line"><span class="pl-s">    A binding model with two components (e.g. Protein and Ligand)</span></td>
      </tr>
      <tr>
        <td id="L280" class="blob-num js-line-number" data-line-number="280"></td>
        <td id="LC280" class="blob-code js-file-line"><span class="pl-s">    <span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L281" class="blob-num js-line-number" data-line-number="281"></td>
        <td id="LC281" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L282" class="blob-num js-line-number" data-line-number="282"></td>
        <td id="LC282" class="blob-code js-file-line">    <span class="pl-k">def</span> <span class="pl-en"><span class="pl-c1">__init__</span></span>(<span class="pl-smi">self</span>, <span class="pl-smi">experiment</span>):</td>
      </tr>
      <tr>
        <td id="L283" class="blob-num js-line-number" data-line-number="283"></td>
        <td id="LC283" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L284" class="blob-num js-line-number" data-line-number="284"></td>
        <td id="LC284" class="blob-code js-file-line">        <span class="pl-c"># Determine number of observations.</span></td>
      </tr>
      <tr>
        <td id="L285" class="blob-num js-line-number" data-line-number="285"></td>
        <td id="LC285" class="blob-code js-file-line">        <span class="pl-v">self</span>.N <span class="pl-k">=</span> experiment.number_of_injections</td>
      </tr>
      <tr>
        <td id="L286" class="blob-num js-line-number" data-line-number="286"></td>
        <td id="LC286" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L287" class="blob-num js-line-number" data-line-number="287"></td>
        <td id="LC287" class="blob-code js-file-line">        <span class="pl-c"># Store injection volumes</span></td>
      </tr>
      <tr>
        <td id="L288" class="blob-num js-line-number" data-line-number="288"></td>
        <td id="LC288" class="blob-code js-file-line">        <span class="pl-v">self</span>.DeltaVn <span class="pl-k">=</span> Quantity(numpy.zeros(<span class="pl-v">self</span>.N), ureg.liter)</td>
      </tr>
      <tr>
        <td id="L289" class="blob-num js-line-number" data-line-number="289"></td>
        <td id="LC289" class="blob-code js-file-line">        <span class="pl-k">for</span> inj, injection <span class="pl-k">in</span> <span class="pl-c1">enumerate</span>(experiment.injections):</td>
      </tr>
      <tr>
        <td id="L290" class="blob-num js-line-number" data-line-number="290"></td>
        <td id="LC290" class="blob-code js-file-line">            <span class="pl-v">self</span>.DeltaVn[inj] <span class="pl-k">=</span> injection.volume</td>
      </tr>
      <tr>
        <td id="L291" class="blob-num js-line-number" data-line-number="291"></td>
        <td id="LC291" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L292" class="blob-num js-line-number" data-line-number="292"></td>
        <td id="LC292" class="blob-code js-file-line">        <span class="pl-c"># Store calorimeter properties.</span></td>
      </tr>
      <tr>
        <td id="L293" class="blob-num js-line-number" data-line-number="293"></td>
        <td id="LC293" class="blob-code js-file-line">        <span class="pl-v">self</span>.V0 <span class="pl-k">=</span> experiment.cell_volume.to(<span class="pl-s"><span class="pl-pds">&#39;</span>liter<span class="pl-pds">&#39;</span></span>)</td>
      </tr>
      <tr>
        <td id="L294" class="blob-num js-line-number" data-line-number="294"></td>
        <td id="LC294" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L295" class="blob-num js-line-number" data-line-number="295"></td>
        <td id="LC295" class="blob-code js-file-line">        <span class="pl-c"># Extract properties from experiment</span></td>
      </tr>
      <tr>
        <td id="L296" class="blob-num js-line-number" data-line-number="296"></td>
        <td id="LC296" class="blob-code js-file-line">        <span class="pl-v">self</span>.experiment <span class="pl-k">=</span> experiment</td>
      </tr>
      <tr>
        <td id="L297" class="blob-num js-line-number" data-line-number="297"></td>
        <td id="LC297" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L298" class="blob-num js-line-number" data-line-number="298"></td>
        <td id="LC298" class="blob-code js-file-line">        <span class="pl-c"># Store temperature.</span></td>
      </tr>
      <tr>
        <td id="L299" class="blob-num js-line-number" data-line-number="299"></td>
        <td id="LC299" class="blob-code js-file-line">        <span class="pl-v">self</span>.temperature <span class="pl-k">=</span> experiment.target_temperature  <span class="pl-c"># (kelvin)</span></td>
      </tr>
      <tr>
        <td id="L300" class="blob-num js-line-number" data-line-number="300"></td>
        <td id="LC300" class="blob-code js-file-line">        <span class="pl-c"># inverse temperature 1/(kcal/mol)</span></td>
      </tr>
      <tr>
        <td id="L301" class="blob-num js-line-number" data-line-number="301"></td>
        <td id="LC301" class="blob-code js-file-line">        <span class="pl-v">self</span>.beta <span class="pl-k">=</span> <span class="pl-c1">1.0</span> <span class="pl-k">/</span> (ureg.molar_gas_constant <span class="pl-k">*</span> <span class="pl-v">self</span>.temperature)</td>
      </tr>
      <tr>
        <td id="L302" class="blob-num js-line-number" data-line-number="302"></td>
        <td id="LC302" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L303" class="blob-num js-line-number" data-line-number="303"></td>
        <td id="LC303" class="blob-code js-file-line">        <span class="pl-c"># Syringe concentration</span></td>
      </tr>
      <tr>
        <td id="L304" class="blob-num js-line-number" data-line-number="304"></td>
        <td id="LC304" class="blob-code js-file-line">        <span class="pl-k">if</span> <span class="pl-k">not</span> <span class="pl-c1">len</span>(experiment.syringe_concentration) <span class="pl-k">==</span> <span class="pl-c1">1</span>:</td>
      </tr>
      <tr>
        <td id="L305" class="blob-num js-line-number" data-line-number="305"></td>
        <td id="LC305" class="blob-code js-file-line">            <span class="pl-k">raise</span> <span class="pl-c1">ValueError</span>(<span class="pl-s"><span class="pl-pds">&#39;</span>TwoComponent model only supports one component in the syringe, found <span class="pl-c1">%d</span><span class="pl-pds">&#39;</span></span> <span class="pl-k">%</span> <span class="pl-c1">len</span>(experiment.syringe_concentration))</td>
      </tr>
      <tr>
        <td id="L306" class="blob-num js-line-number" data-line-number="306"></td>
        <td id="LC306" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L307" class="blob-num js-line-number" data-line-number="307"></td>
        <td id="LC307" class="blob-code js-file-line">        Ls_stated <span class="pl-k">=</span> <span class="pl-v">self</span>._get_syringe_concentration(experiment)</td>
      </tr>
      <tr>
        <td id="L308" class="blob-num js-line-number" data-line-number="308"></td>
        <td id="LC308" class="blob-code js-file-line">        <span class="pl-c"># Uncertainty</span></td>
      </tr>
      <tr>
        <td id="L309" class="blob-num js-line-number" data-line-number="309"></td>
        <td id="LC309" class="blob-code js-file-line">        dLs <span class="pl-k">=</span> <span class="pl-c1">0.10</span> <span class="pl-k">*</span> Ls_stated</td>
      </tr>
      <tr>
        <td id="L310" class="blob-num js-line-number" data-line-number="310"></td>
        <td id="LC310" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L311" class="blob-num js-line-number" data-line-number="311"></td>
        <td id="LC311" class="blob-code js-file-line">        <span class="pl-c">#Cell concentrations</span></td>
      </tr>
      <tr>
        <td id="L312" class="blob-num js-line-number" data-line-number="312"></td>
        <td id="LC312" class="blob-code js-file-line">        <span class="pl-k">if</span> <span class="pl-k">not</span> <span class="pl-c1">len</span>(experiment.cell_concentration) <span class="pl-k">==</span> <span class="pl-c1">1</span>:</td>
      </tr>
      <tr>
        <td id="L313" class="blob-num js-line-number" data-line-number="313"></td>
        <td id="LC313" class="blob-code js-file-line">            <span class="pl-k">raise</span> <span class="pl-c1">ValueError</span>(<span class="pl-s"><span class="pl-pds">&#39;</span>TwoComponent model only supports one component in the cell, found <span class="pl-c1">%d</span><span class="pl-pds">&#39;</span></span> <span class="pl-k">%</span> <span class="pl-c1">len</span>(experiment.cell_concentration))</td>
      </tr>
      <tr>
        <td id="L314" class="blob-num js-line-number" data-line-number="314"></td>
        <td id="LC314" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L315" class="blob-num js-line-number" data-line-number="315"></td>
        <td id="LC315" class="blob-code js-file-line">        P0_stated <span class="pl-k">=</span> <span class="pl-v">self</span>._get_cell_concentration(experiment)</td>
      </tr>
      <tr>
        <td id="L316" class="blob-num js-line-number" data-line-number="316"></td>
        <td id="LC316" class="blob-code js-file-line">        <span class="pl-c"># Uncertainty</span></td>
      </tr>
      <tr>
        <td id="L317" class="blob-num js-line-number" data-line-number="317"></td>
        <td id="LC317" class="blob-code js-file-line">        dP0 <span class="pl-k">=</span> <span class="pl-c1">0.10</span> <span class="pl-k">*</span> P0_stated</td>
      </tr>
      <tr>
        <td id="L318" class="blob-num js-line-number" data-line-number="318"></td>
        <td id="LC318" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L319" class="blob-num js-line-number" data-line-number="319"></td>
        <td id="LC319" class="blob-code js-file-line">        <span class="pl-c"># Define priors for concentrations.</span></td>
      </tr>
      <tr>
        <td id="L320" class="blob-num js-line-number" data-line-number="320"></td>
        <td id="LC320" class="blob-code js-file-line">        <span class="pl-v">self</span>.P0 <span class="pl-k">=</span> BindingModel._lognormal_concentration_prior(<span class="pl-s"><span class="pl-pds">&#39;</span>P0<span class="pl-pds">&#39;</span></span>, P0_stated, dP0, ureg.millimolar)</td>
      </tr>
      <tr>
        <td id="L321" class="blob-num js-line-number" data-line-number="321"></td>
        <td id="LC321" class="blob-code js-file-line">        <span class="pl-v">self</span>.Ls <span class="pl-k">=</span> BindingModel._lognormal_concentration_prior(<span class="pl-s"><span class="pl-pds">&#39;</span>Ls<span class="pl-pds">&#39;</span></span>, Ls_stated, dLs, ureg.millimolar)</td>
      </tr>
      <tr>
        <td id="L322" class="blob-num js-line-number" data-line-number="322"></td>
        <td id="LC322" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L323" class="blob-num js-line-number" data-line-number="323"></td>
        <td id="LC323" class="blob-code js-file-line">        <span class="pl-c"># Extract heats from experiment</span></td>
      </tr>
      <tr>
        <td id="L324" class="blob-num js-line-number" data-line-number="324"></td>
        <td id="LC324" class="blob-code js-file-line">        q_n <span class="pl-k">=</span> Quantity(numpy.zeros(<span class="pl-c1">len</span>(experiment.injections)), <span class="pl-s"><span class="pl-pds">&#39;</span>calorie<span class="pl-pds">&#39;</span></span>)</td>
      </tr>
      <tr>
        <td id="L325" class="blob-num js-line-number" data-line-number="325"></td>
        <td id="LC325" class="blob-code js-file-line">        <span class="pl-k">for</span> inj, injection <span class="pl-k">in</span> <span class="pl-c1">enumerate</span>(experiment.injections):</td>
      </tr>
      <tr>
        <td id="L326" class="blob-num js-line-number" data-line-number="326"></td>
        <td id="LC326" class="blob-code js-file-line">            q_n[inj] <span class="pl-k">=</span> injection.evolved_heat</td>
      </tr>
      <tr>
        <td id="L327" class="blob-num js-line-number" data-line-number="327"></td>
        <td id="LC327" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L328" class="blob-num js-line-number" data-line-number="328"></td>
        <td id="LC328" class="blob-code js-file-line">        <span class="pl-c"># Guess for the noise parameter log(sigma)</span></td>
      </tr>
      <tr>
        <td id="L329" class="blob-num js-line-number" data-line-number="329"></td>
        <td id="LC329" class="blob-code js-file-line">        log_sigma_guess, log_sigma_max, log_sigma_min <span class="pl-k">=</span> <span class="pl-v">self</span>._logsigma_guesses(q_n, <span class="pl-c1">4</span>, ureg.calorie)</td>
      </tr>
      <tr>
        <td id="L330" class="blob-num js-line-number" data-line-number="330"></td>
        <td id="LC330" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L331" class="blob-num js-line-number" data-line-number="331"></td>
        <td id="LC331" class="blob-code js-file-line">        <span class="pl-c"># Determine range for priors for thermodynamic parameters.</span></td>
      </tr>
      <tr>
        <td id="L332" class="blob-num js-line-number" data-line-number="332"></td>
        <td id="LC332" class="blob-code js-file-line">        <span class="pl-c"># TODO add literature value guesses</span></td>
      </tr>
      <tr>
        <td id="L333" class="blob-num js-line-number" data-line-number="333"></td>
        <td id="LC333" class="blob-code js-file-line">        <span class="pl-c"># review check out all the units to make sure that they&#39;re appropriate</span></td>
      </tr>
      <tr>
        <td id="L334" class="blob-num js-line-number" data-line-number="334"></td>
        <td id="LC334" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L335" class="blob-num js-line-number" data-line-number="335"></td>
        <td id="LC335" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L336" class="blob-num js-line-number" data-line-number="336"></td>
        <td id="LC336" class="blob-code js-file-line">        <span class="pl-v">self</span>.DeltaH_0 <span class="pl-k">=</span> BindingModel._uniform_prior_with_guesses_and_units(<span class="pl-s"><span class="pl-pds">&#39;</span>DeltaH_0<span class="pl-pds">&#39;</span></span>, <span class="pl-k">*</span><span class="pl-v">self</span>._deltaH0_guesses(q_n), <span class="pl-smi">prior_unit</span><span class="pl-k">=</span>ureg.calorie, <span class="pl-smi">guess_unit</span><span class="pl-k">=</span><span class="pl-c1">True</span>)</td>
      </tr>
      <tr>
        <td id="L337" class="blob-num js-line-number" data-line-number="337"></td>
        <td id="LC337" class="blob-code js-file-line">        <span class="pl-v">self</span>.DeltaG <span class="pl-k">=</span> BindingModel._uniform_prior_with_guesses_and_units(<span class="pl-s"><span class="pl-pds">&#39;</span>DeltaG<span class="pl-pds">&#39;</span></span>, <span class="pl-c1">0.</span>, <span class="pl-c1">40.</span>, <span class="pl-k">-</span><span class="pl-c1">40.</span>, ureg.kilocalorie<span class="pl-k">/</span>ureg.mole)</td>
      </tr>
      <tr>
        <td id="L338" class="blob-num js-line-number" data-line-number="338"></td>
        <td id="LC338" class="blob-code js-file-line">        <span class="pl-v">self</span>.DeltaH <span class="pl-k">=</span> BindingModel._uniform_prior_with_guesses_and_units(<span class="pl-s"><span class="pl-pds">&#39;</span>DeltaH<span class="pl-pds">&#39;</span></span>, <span class="pl-c1">0.</span>, <span class="pl-c1">100.</span>, <span class="pl-k">-</span><span class="pl-c1">100.</span>, ureg.kilocalorie<span class="pl-k">/</span>ureg.mole)</td>
      </tr>
      <tr>
        <td id="L339" class="blob-num js-line-number" data-line-number="339"></td>
        <td id="LC339" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L340" class="blob-num js-line-number" data-line-number="340"></td>
        <td id="LC340" class="blob-code js-file-line">        <span class="pl-c"># Define priors for thermodynamic quantities.</span></td>
      </tr>
      <tr>
        <td id="L341" class="blob-num js-line-number" data-line-number="341"></td>
        <td id="LC341" class="blob-code js-file-line">        <span class="pl-v">self</span>.log_sigma <span class="pl-k">=</span> BindingModel._uniform_prior(<span class="pl-s"><span class="pl-pds">&#39;</span>log_sigma<span class="pl-pds">&#39;</span></span>, log_sigma_guess, log_sigma_max, log_sigma_min)</td>
      </tr>
      <tr>
        <td id="L342" class="blob-num js-line-number" data-line-number="342"></td>
        <td id="LC342" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L343" class="blob-num js-line-number" data-line-number="343"></td>
        <td id="LC343" class="blob-code js-file-line">        <span class="pl-c"># Define the model</span></td>
      </tr>
      <tr>
        <td id="L344" class="blob-num js-line-number" data-line-number="344"></td>
        <td id="LC344" class="blob-code js-file-line">        q_n_model <span class="pl-k">=</span> <span class="pl-v">self</span>._lambda_heats_model()</td>
      </tr>
      <tr>
        <td id="L345" class="blob-num js-line-number" data-line-number="345"></td>
        <td id="LC345" class="blob-code js-file-line">        tau <span class="pl-k">=</span> <span class="pl-v">self</span>._lambda_tau_model()</td>
      </tr>
      <tr>
        <td id="L346" class="blob-num js-line-number" data-line-number="346"></td>
        <td id="LC346" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L347" class="blob-num js-line-number" data-line-number="347"></td>
        <td id="LC347" class="blob-code js-file-line">        <span class="pl-c"># Set observation</span></td>
      </tr>
      <tr>
        <td id="L348" class="blob-num js-line-number" data-line-number="348"></td>
        <td id="LC348" class="blob-code js-file-line">        <span class="pl-v">self</span>.q_n_obs <span class="pl-k">=</span> BindingModel._normal_observation_with_units(<span class="pl-s"><span class="pl-pds">&#39;</span>q_n<span class="pl-pds">&#39;</span></span>, q_n_model, q_n, tau, ureg.microcalorie <span class="pl-k">/</span> ureg.mole)</td>
      </tr>
      <tr>
        <td id="L349" class="blob-num js-line-number" data-line-number="349"></td>
        <td id="LC349" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L350" class="blob-num js-line-number" data-line-number="350"></td>
        <td id="LC350" class="blob-code js-file-line">        <span class="pl-c"># Create sampler.</span></td>
      </tr>
      <tr>
        <td id="L351" class="blob-num js-line-number" data-line-number="351"></td>
        <td id="LC351" class="blob-code js-file-line">        <span class="pl-v">self</span>.mcmc <span class="pl-k">=</span> <span class="pl-v">self</span>._create_metropolis_sampler(Ls_stated, P0_stated, experiment)</td>
      </tr>
      <tr>
        <td id="L352" class="blob-num js-line-number" data-line-number="352"></td>
        <td id="LC352" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L353" class="blob-num js-line-number" data-line-number="353"></td>
        <td id="LC353" class="blob-code js-file-line">        <span class="pl-k">return</span></td>
      </tr>
      <tr>
        <td id="L354" class="blob-num js-line-number" data-line-number="354"></td>
        <td id="LC354" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L355" class="blob-num js-line-number" data-line-number="355"></td>
        <td id="LC355" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L356" class="blob-num js-line-number" data-line-number="356"></td>
        <td id="LC356" class="blob-code js-file-line">    <span class="pl-en">@<span class="pl-c1">staticmethod</span></span></td>
      </tr>
      <tr>
        <td id="L357" class="blob-num js-line-number" data-line-number="357"></td>
        <td id="LC357" class="blob-code js-file-line">    <span class="pl-en">@</span><span class="pl-en">ureg.wraps</span>(<span class="pl-smi">ret</span><span class="pl-k">=</span>ureg.calorie, <span class="pl-smi">args</span><span class="pl-k">=</span>[ureg.liter, ureg.liter, <span class="pl-c1">None</span>, <span class="pl-c1">None</span>, <span class="pl-c1">None</span>, <span class="pl-c1">None</span>, <span class="pl-c1">None</span>,  ureg.mole <span class="pl-k">/</span> ureg.kilocalories, <span class="pl-c1">None</span>], <span class="pl-smi">strict</span><span class="pl-k">=</span><span class="pl-c1">True</span>)</td>
      </tr>
      <tr>
        <td id="L358" class="blob-num js-line-number" data-line-number="358"></td>
        <td id="LC358" class="blob-code js-file-line">    <span class="pl-k">def</span> <span class="pl-en">expected_injection_heats</span>(<span class="pl-smi">V0</span>, <span class="pl-smi">DeltaVn</span>, <span class="pl-smi">P0</span>, <span class="pl-smi">Ls</span>, <span class="pl-smi">DeltaG</span>, <span class="pl-smi">DeltaH</span>, <span class="pl-smi">DeltaH_0</span>, <span class="pl-smi">beta</span>, <span class="pl-smi">N</span>):</td>
      </tr>
      <tr>
        <td id="L359" class="blob-num js-line-number" data-line-number="359"></td>
        <td id="LC359" class="blob-code js-file-line">        <span class="pl-s"><span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L360" class="blob-num js-line-number" data-line-number="360"></td>
        <td id="LC360" class="blob-code js-file-line"><span class="pl-s">        Expected heats of injection for two-component binding model.</span></td>
      </tr>
      <tr>
        <td id="L361" class="blob-num js-line-number" data-line-number="361"></td>
        <td id="LC361" class="blob-code js-file-line"><span class="pl-s">        ARGUMENTS</span></td>
      </tr>
      <tr>
        <td id="L362" class="blob-num js-line-number" data-line-number="362"></td>
        <td id="LC362" class="blob-code js-file-line"><span class="pl-s">        V0 - cell volume (liter)</span></td>
      </tr>
      <tr>
        <td id="L363" class="blob-num js-line-number" data-line-number="363"></td>
        <td id="LC363" class="blob-code js-file-line"><span class="pl-s">        DeltaVn - injection volumes (liter)</span></td>
      </tr>
      <tr>
        <td id="L364" class="blob-num js-line-number" data-line-number="364"></td>
        <td id="LC364" class="blob-code js-file-line"><span class="pl-s">        P0 - Cell concentration (millimolar)</span></td>
      </tr>
      <tr>
        <td id="L365" class="blob-num js-line-number" data-line-number="365"></td>
        <td id="LC365" class="blob-code js-file-line"><span class="pl-s">        Ls - Syringe concentration (millimolar)</span></td>
      </tr>
      <tr>
        <td id="L366" class="blob-num js-line-number" data-line-number="366"></td>
        <td id="LC366" class="blob-code js-file-line"><span class="pl-s">        DeltaG - free energy of binding (kcal/mol)</span></td>
      </tr>
      <tr>
        <td id="L367" class="blob-num js-line-number" data-line-number="367"></td>
        <td id="LC367" class="blob-code js-file-line"><span class="pl-s">        DeltaH - enthalpy of binding (kcal/mol)</span></td>
      </tr>
      <tr>
        <td id="L368" class="blob-num js-line-number" data-line-number="368"></td>
        <td id="LC368" class="blob-code js-file-line"><span class="pl-s">        DeltaH_0 - heat of injection (cal)</span></td>
      </tr>
      <tr>
        <td id="L369" class="blob-num js-line-number" data-line-number="369"></td>
        <td id="LC369" class="blob-code js-file-line"><span class="pl-s">        beta - inverse temperature * gas constant (mole / kcal)</span></td>
      </tr>
      <tr>
        <td id="L370" class="blob-num js-line-number" data-line-number="370"></td>
        <td id="LC370" class="blob-code js-file-line"><span class="pl-s">        N - number of injections</span></td>
      </tr>
      <tr>
        <td id="L371" class="blob-num js-line-number" data-line-number="371"></td>
        <td id="LC371" class="blob-code js-file-line"><span class="pl-s">        Returns</span></td>
      </tr>
      <tr>
        <td id="L372" class="blob-num js-line-number" data-line-number="372"></td>
        <td id="LC372" class="blob-code js-file-line"><span class="pl-s">        -------</span></td>
      </tr>
      <tr>
        <td id="L373" class="blob-num js-line-number" data-line-number="373"></td>
        <td id="LC373" class="blob-code js-file-line"><span class="pl-s">        expected injection heats -</span></td>
      </tr>
      <tr>
        <td id="L374" class="blob-num js-line-number" data-line-number="374"></td>
        <td id="LC374" class="blob-code js-file-line"><span class="pl-s">        <span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L375" class="blob-num js-line-number" data-line-number="375"></td>
        <td id="LC375" class="blob-code js-file-line">        <span class="pl-c"># TODO Units that go into this need to be verified</span></td>
      </tr>
      <tr>
        <td id="L376" class="blob-num js-line-number" data-line-number="376"></td>
        <td id="LC376" class="blob-code js-file-line">        <span class="pl-c"># TODO update docstring with new input</span></td>
      </tr>
      <tr>
        <td id="L377" class="blob-num js-line-number" data-line-number="377"></td>
        <td id="LC377" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L378" class="blob-num js-line-number" data-line-number="378"></td>
        <td id="LC378" class="blob-code js-file-line">        Kd <span class="pl-k">=</span> exp(beta <span class="pl-k">*</span> DeltaG)   <span class="pl-c"># dissociation constant (M)</span></td>
      </tr>
      <tr>
        <td id="L379" class="blob-num js-line-number" data-line-number="379"></td>
        <td id="LC379" class="blob-code js-file-line">        N <span class="pl-k">=</span> N</td>
      </tr>
      <tr>
        <td id="L380" class="blob-num js-line-number" data-line-number="380"></td>
        <td id="LC380" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L381" class="blob-num js-line-number" data-line-number="381"></td>
        <td id="LC381" class="blob-code js-file-line">        <span class="pl-c"># Compute complex concentrations.</span></td>
      </tr>
      <tr>
        <td id="L382" class="blob-num js-line-number" data-line-number="382"></td>
        <td id="LC382" class="blob-code js-file-line">        <span class="pl-c"># Pn[n] is the protein concentration in sample cell after n injections</span></td>
      </tr>
      <tr>
        <td id="L383" class="blob-num js-line-number" data-line-number="383"></td>
        <td id="LC383" class="blob-code js-file-line">        <span class="pl-c"># (M)</span></td>
      </tr>
      <tr>
        <td id="L384" class="blob-num js-line-number" data-line-number="384"></td>
        <td id="LC384" class="blob-code js-file-line">        Pn <span class="pl-k">=</span> numpy.zeros([N])</td>
      </tr>
      <tr>
        <td id="L385" class="blob-num js-line-number" data-line-number="385"></td>
        <td id="LC385" class="blob-code js-file-line">        <span class="pl-c"># Ln[n] is the ligand concentration in sample cell after n injections</span></td>
      </tr>
      <tr>
        <td id="L386" class="blob-num js-line-number" data-line-number="386"></td>
        <td id="LC386" class="blob-code js-file-line">        <span class="pl-c"># (M)</span></td>
      </tr>
      <tr>
        <td id="L387" class="blob-num js-line-number" data-line-number="387"></td>
        <td id="LC387" class="blob-code js-file-line">        Ln <span class="pl-k">=</span> numpy.zeros([N])</td>
      </tr>
      <tr>
        <td id="L388" class="blob-num js-line-number" data-line-number="388"></td>
        <td id="LC388" class="blob-code js-file-line">        <span class="pl-c"># PLn[n] is the complex concentration in sample cell after n injections</span></td>
      </tr>
      <tr>
        <td id="L389" class="blob-num js-line-number" data-line-number="389"></td>
        <td id="LC389" class="blob-code js-file-line">        <span class="pl-c"># (M)</span></td>
      </tr>
      <tr>
        <td id="L390" class="blob-num js-line-number" data-line-number="390"></td>
        <td id="LC390" class="blob-code js-file-line">        PLn <span class="pl-k">=</span> numpy.zeros([N])</td>
      </tr>
      <tr>
        <td id="L391" class="blob-num js-line-number" data-line-number="391"></td>
        <td id="LC391" class="blob-code js-file-line">        dcum <span class="pl-k">=</span> <span class="pl-c1">1.0</span>  <span class="pl-c"># cumulative dilution factor (dimensionless)</span></td>
      </tr>
      <tr>
        <td id="L392" class="blob-num js-line-number" data-line-number="392"></td>
        <td id="LC392" class="blob-code js-file-line">        <span class="pl-k">for</span> n <span class="pl-k">in</span> <span class="pl-c1">range</span>(N):</td>
      </tr>
      <tr>
        <td id="L393" class="blob-num js-line-number" data-line-number="393"></td>
        <td id="LC393" class="blob-code js-file-line">            <span class="pl-c"># Instantaneous injection model (perfusion)</span></td>
      </tr>
      <tr>
        <td id="L394" class="blob-num js-line-number" data-line-number="394"></td>
        <td id="LC394" class="blob-code js-file-line">            <span class="pl-c"># TODO: Allow injection volume to vary for each injection.</span></td>
      </tr>
      <tr>
        <td id="L395" class="blob-num js-line-number" data-line-number="395"></td>
        <td id="LC395" class="blob-code js-file-line">            <span class="pl-c"># dilution factor for this injection (dimensionless)</span></td>
      </tr>
      <tr>
        <td id="L396" class="blob-num js-line-number" data-line-number="396"></td>
        <td id="LC396" class="blob-code js-file-line">            d <span class="pl-k">=</span> <span class="pl-c1">1.0</span> <span class="pl-k">-</span> (DeltaVn[n] <span class="pl-k">/</span> V0)</td>
      </tr>
      <tr>
        <td id="L397" class="blob-num js-line-number" data-line-number="397"></td>
        <td id="LC397" class="blob-code js-file-line">            dcum <span class="pl-k">*=</span> d  <span class="pl-c"># cumulative dilution factor</span></td>
      </tr>
      <tr>
        <td id="L398" class="blob-num js-line-number" data-line-number="398"></td>
        <td id="LC398" class="blob-code js-file-line">            <span class="pl-c"># total quantity of protein in sample cell after n injections (mol)</span></td>
      </tr>
      <tr>
        <td id="L399" class="blob-num js-line-number" data-line-number="399"></td>
        <td id="LC399" class="blob-code js-file-line">            P <span class="pl-k">=</span> V0 <span class="pl-k">*</span> P0 <span class="pl-k">*</span> <span class="pl-c1">1.e-3</span> <span class="pl-k">*</span> dcum</td>
      </tr>
      <tr>
        <td id="L400" class="blob-num js-line-number" data-line-number="400"></td>
        <td id="LC400" class="blob-code js-file-line">            <span class="pl-c"># total quantity of ligand in sample cell after n injections (mol)</span></td>
      </tr>
      <tr>
        <td id="L401" class="blob-num js-line-number" data-line-number="401"></td>
        <td id="LC401" class="blob-code js-file-line">            L <span class="pl-k">=</span> V0 <span class="pl-k">*</span> Ls <span class="pl-k">*</span> <span class="pl-c1">1.e-3</span> <span class="pl-k">*</span> (<span class="pl-c1">1.</span> <span class="pl-k">-</span> dcum)</td>
      </tr>
      <tr>
        <td id="L402" class="blob-num js-line-number" data-line-number="402"></td>
        <td id="LC402" class="blob-code js-file-line">            <span class="pl-c"># complex concentration (M)</span></td>
      </tr>
      <tr>
        <td id="L403" class="blob-num js-line-number" data-line-number="403"></td>
        <td id="LC403" class="blob-code js-file-line">            PLn[n] <span class="pl-k">=</span> (<span class="pl-c1">0.5</span> <span class="pl-k">/</span> V0 <span class="pl-k">*</span> ((P <span class="pl-k">+</span> L <span class="pl-k">+</span> Kd <span class="pl-k">*</span> V0) <span class="pl-k">-</span> ((P <span class="pl-k">+</span> L <span class="pl-k">+</span> Kd <span class="pl-k">*</span> V0) <span class="pl-k">**</span> <span class="pl-c1">2</span> <span class="pl-k">-</span> <span class="pl-c1">4</span> <span class="pl-k">*</span> P <span class="pl-k">*</span> L) <span class="pl-k">**</span> <span class="pl-c1">0.5</span>))</td>
      </tr>
      <tr>
        <td id="L404" class="blob-num js-line-number" data-line-number="404"></td>
        <td id="LC404" class="blob-code js-file-line">            <span class="pl-c"># free protein concentration in sample cell after n injections (M)</span></td>
      </tr>
      <tr>
        <td id="L405" class="blob-num js-line-number" data-line-number="405"></td>
        <td id="LC405" class="blob-code js-file-line">            Pn[n] <span class="pl-k">=</span> P <span class="pl-k">/</span> V0 <span class="pl-k">-</span> PLn[n]</td>
      </tr>
      <tr>
        <td id="L406" class="blob-num js-line-number" data-line-number="406"></td>
        <td id="LC406" class="blob-code js-file-line">            <span class="pl-c"># free ligand concentration in sample cell after n injections (M)</span></td>
      </tr>
      <tr>
        <td id="L407" class="blob-num js-line-number" data-line-number="407"></td>
        <td id="LC407" class="blob-code js-file-line">            Ln[n] <span class="pl-k">=</span> L <span class="pl-k">/</span> V0 <span class="pl-k">-</span> PLn[n]</td>
      </tr>
      <tr>
        <td id="L408" class="blob-num js-line-number" data-line-number="408"></td>
        <td id="LC408" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L409" class="blob-num js-line-number" data-line-number="409"></td>
        <td id="LC409" class="blob-code js-file-line">        <span class="pl-c"># Compute expected injection heats.</span></td>
      </tr>
      <tr>
        <td id="L410" class="blob-num js-line-number" data-line-number="410"></td>
        <td id="LC410" class="blob-code js-file-line">        <span class="pl-c"># q_n_model[n] is the expected heat from injection n</span></td>
      </tr>
      <tr>
        <td id="L411" class="blob-num js-line-number" data-line-number="411"></td>
        <td id="LC411" class="blob-code js-file-line">        q_n <span class="pl-k">=</span> numpy.zeros([N])</td>
      </tr>
      <tr>
        <td id="L412" class="blob-num js-line-number" data-line-number="412"></td>
        <td id="LC412" class="blob-code js-file-line">        <span class="pl-c"># Instantaneous injection model (perfusion)</span></td>
      </tr>
      <tr>
        <td id="L413" class="blob-num js-line-number" data-line-number="413"></td>
        <td id="LC413" class="blob-code js-file-line">        <span class="pl-c"># first injection</span></td>
      </tr>
      <tr>
        <td id="L414" class="blob-num js-line-number" data-line-number="414"></td>
        <td id="LC414" class="blob-code js-file-line">        q_n[<span class="pl-c1">0</span>] <span class="pl-k">=</span> (DeltaH <span class="pl-k">*</span> V0 <span class="pl-k">*</span> PLn[<span class="pl-c1">0</span>])<span class="pl-k">*</span><span class="pl-c1">1000</span> <span class="pl-k">+</span> DeltaH_0</td>
      </tr>
      <tr>
        <td id="L415" class="blob-num js-line-number" data-line-number="415"></td>
        <td id="LC415" class="blob-code js-file-line">        <span class="pl-k">for</span> n <span class="pl-k">in</span> <span class="pl-c1">range</span>(<span class="pl-c1">1</span>, N):</td>
      </tr>
      <tr>
        <td id="L416" class="blob-num js-line-number" data-line-number="416"></td>
        <td id="LC416" class="blob-code js-file-line">            d <span class="pl-k">=</span> <span class="pl-c1">1.0</span> <span class="pl-k">-</span> (DeltaVn[n] <span class="pl-k">/</span> V0)  <span class="pl-c"># dilution factor (dimensionless)</span></td>
      </tr>
      <tr>
        <td id="L417" class="blob-num js-line-number" data-line-number="417"></td>
        <td id="LC417" class="blob-code js-file-line">            <span class="pl-c"># subsequent injections</span></td>
      </tr>
      <tr>
        <td id="L418" class="blob-num js-line-number" data-line-number="418"></td>
        <td id="LC418" class="blob-code js-file-line">            q_n[n] <span class="pl-k">=</span> (DeltaH <span class="pl-k">*</span> V0 <span class="pl-k">*</span> (PLn[n] <span class="pl-k">-</span> d <span class="pl-k">*</span> PLn[n <span class="pl-k">-</span> <span class="pl-c1">1</span>])) <span class="pl-k">*</span> <span class="pl-c1">1000</span> <span class="pl-k">+</span> DeltaH_0</td>
      </tr>
      <tr>
        <td id="L419" class="blob-num js-line-number" data-line-number="419"></td>
        <td id="LC419" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L420" class="blob-num js-line-number" data-line-number="420"></td>
        <td id="LC420" class="blob-code js-file-line">        <span class="pl-k">return</span> q_n</td>
      </tr>
      <tr>
        <td id="L421" class="blob-num js-line-number" data-line-number="421"></td>
        <td id="LC421" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L422" class="blob-num js-line-number" data-line-number="422"></td>
        <td id="LC422" class="blob-code js-file-line">    <span class="pl-en">@<span class="pl-c1">staticmethod</span></span></td>
      </tr>
      <tr>
        <td id="L423" class="blob-num js-line-number" data-line-number="423"></td>
        <td id="LC423" class="blob-code js-file-line">    <span class="pl-k">def</span> <span class="pl-en">tau</span>(<span class="pl-smi">log_sigma</span>):</td>
      </tr>
      <tr>
        <td id="L424" class="blob-num js-line-number" data-line-number="424"></td>
        <td id="LC424" class="blob-code js-file-line">        <span class="pl-s"><span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L425" class="blob-num js-line-number" data-line-number="425"></td>
        <td id="LC425" class="blob-code js-file-line"><span class="pl-s">        Injection heat measurement precision.</span></td>
      </tr>
      <tr>
        <td id="L426" class="blob-num js-line-number" data-line-number="426"></td>
        <td id="LC426" class="blob-code js-file-line"><span class="pl-s">        <span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L427" class="blob-num js-line-number" data-line-number="427"></td>
        <td id="LC427" class="blob-code js-file-line">        <span class="pl-k">return</span> numpy.exp(<span class="pl-k">-</span><span class="pl-c1">2.0</span> <span class="pl-k">*</span> log_sigma)</td>
      </tr>
      <tr>
        <td id="L428" class="blob-num js-line-number" data-line-number="428"></td>
        <td id="LC428" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L429" class="blob-num js-line-number" data-line-number="429"></td>
        <td id="LC429" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L430" class="blob-num js-line-number" data-line-number="430"></td>
        <td id="LC430" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L431" class="blob-num js-line-number" data-line-number="431"></td>
        <td id="LC431" class="blob-code js-file-line">    <span class="pl-k">def</span> <span class="pl-en">_create_rescaling_sampler</span>(<span class="pl-smi">self</span>, <span class="pl-smi">Ls_stated</span>, <span class="pl-smi">P0_stated</span>, <span class="pl-smi">experiment</span>):</td>
      </tr>
      <tr>
        <td id="L432" class="blob-num js-line-number" data-line-number="432"></td>
        <td id="LC432" class="blob-code js-file-line">        <span class="pl-s"><span class="pl-pds">&quot;&quot;&quot;</span>Create an MCMC sampler for the two component model.</span></td>
      </tr>
      <tr>
        <td id="L433" class="blob-num js-line-number" data-line-number="433"></td>
        <td id="LC433" class="blob-code js-file-line"><span class="pl-s">           Uses rescalingstep only when concentrations exist for both P and L.<span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L434" class="blob-num js-line-number" data-line-number="434"></td>
        <td id="LC434" class="blob-code js-file-line">        mcmc <span class="pl-k">=</span> <span class="pl-v">self</span>._create_metropolis_sampler(Ls_stated, P0_stated, experiment)</td>
      </tr>
      <tr>
        <td id="L435" class="blob-num js-line-number" data-line-number="435"></td>
        <td id="LC435" class="blob-code js-file-line">        <span class="pl-k">if</span> P0_stated <span class="pl-k">&gt;</span> Quantity(<span class="pl-s"><span class="pl-pds">&#39;</span>0.0 molar<span class="pl-pds">&#39;</span></span>) <span class="pl-k">and</span> Ls_stated <span class="pl-k">&gt;</span> Quantity(<span class="pl-s"><span class="pl-pds">&#39;</span>0.0 molar<span class="pl-pds">&#39;</span></span>):</td>
      </tr>
      <tr>
        <td id="L436" class="blob-num js-line-number" data-line-number="436"></td>
        <td id="LC436" class="blob-code js-file-line">            mcmc.use_step_method(RescalingStep,</td>
      </tr>
      <tr>
        <td id="L437" class="blob-num js-line-number" data-line-number="437"></td>
        <td id="LC437" class="blob-code js-file-line">                                 {<span class="pl-s"><span class="pl-pds">&#39;</span>Ls<span class="pl-pds">&#39;</span></span>: <span class="pl-v">self</span>.Ls,</td>
      </tr>
      <tr>
        <td id="L438" class="blob-num js-line-number" data-line-number="438"></td>
        <td id="LC438" class="blob-code js-file-line">                                  <span class="pl-s"><span class="pl-pds">&#39;</span>P0<span class="pl-pds">&#39;</span></span>: <span class="pl-v">self</span>.P0,</td>
      </tr>
      <tr>
        <td id="L439" class="blob-num js-line-number" data-line-number="439"></td>
        <td id="LC439" class="blob-code js-file-line">                                  <span class="pl-s"><span class="pl-pds">&#39;</span>DeltaH<span class="pl-pds">&#39;</span></span>: <span class="pl-v">self</span>.DeltaH,</td>
      </tr>
      <tr>
        <td id="L440" class="blob-num js-line-number" data-line-number="440"></td>
        <td id="LC440" class="blob-code js-file-line">                                  <span class="pl-s"><span class="pl-pds">&#39;</span>DeltaG<span class="pl-pds">&#39;</span></span>: <span class="pl-v">self</span>.DeltaG},</td>
      </tr>
      <tr>
        <td id="L441" class="blob-num js-line-number" data-line-number="441"></td>
        <td id="LC441" class="blob-code js-file-line">                                 <span class="pl-v">self</span>.beta</td>
      </tr>
      <tr>
        <td id="L442" class="blob-num js-line-number" data-line-number="442"></td>
        <td id="LC442" class="blob-code js-file-line">            )</td>
      </tr>
      <tr>
        <td id="L443" class="blob-num js-line-number" data-line-number="443"></td>
        <td id="LC443" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L444" class="blob-num js-line-number" data-line-number="444"></td>
        <td id="LC444" class="blob-code js-file-line">        <span class="pl-k">return</span> mcmc</td>
      </tr>
      <tr>
        <td id="L445" class="blob-num js-line-number" data-line-number="445"></td>
        <td id="LC445" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L446" class="blob-num js-line-number" data-line-number="446"></td>
        <td id="LC446" class="blob-code js-file-line">    <span class="pl-k">def</span> <span class="pl-en">_create_metropolis_sampler</span>(<span class="pl-smi">self</span>, <span class="pl-smi">Ls_stated</span>, <span class="pl-smi">P0_stated</span>, <span class="pl-smi">experiment</span>):</td>
      </tr>
      <tr>
        <td id="L447" class="blob-num js-line-number" data-line-number="447"></td>
        <td id="LC447" class="blob-code js-file-line">        <span class="pl-s"><span class="pl-pds">&quot;&quot;&quot;</span>Create an MCMC sampler for the two component model.</span></td>
      </tr>
      <tr>
        <td id="L448" class="blob-num js-line-number" data-line-number="448"></td>
        <td id="LC448" class="blob-code js-file-line"><span class="pl-s">        <span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L449" class="blob-num js-line-number" data-line-number="449"></td>
        <td id="LC449" class="blob-code js-file-line">        mcmc <span class="pl-k">=</span> pymc.MCMC(<span class="pl-v">self</span>, <span class="pl-smi">db</span><span class="pl-k">=</span><span class="pl-s"><span class="pl-pds">&#39;</span>ram<span class="pl-pds">&#39;</span></span>)</td>
      </tr>
      <tr>
        <td id="L450" class="blob-num js-line-number" data-line-number="450"></td>
        <td id="LC450" class="blob-code js-file-line">        mcmc.use_step_method(pymc.Metropolis, <span class="pl-v">self</span>.DeltaG)</td>
      </tr>
      <tr>
        <td id="L451" class="blob-num js-line-number" data-line-number="451"></td>
        <td id="LC451" class="blob-code js-file-line">        mcmc.use_step_method(pymc.Metropolis, <span class="pl-v">self</span>.DeltaH)</td>
      </tr>
      <tr>
        <td id="L452" class="blob-num js-line-number" data-line-number="452"></td>
        <td id="LC452" class="blob-code js-file-line">        mcmc.use_step_method(pymc.Metropolis, <span class="pl-v">self</span>.DeltaH_0)</td>
      </tr>
      <tr>
        <td id="L453" class="blob-num js-line-number" data-line-number="453"></td>
        <td id="LC453" class="blob-code js-file-line">        <span class="pl-k">if</span> P0_stated <span class="pl-k">&gt;</span> Quantity(<span class="pl-s"><span class="pl-pds">&#39;</span>0.0 molar<span class="pl-pds">&#39;</span></span>):</td>
      </tr>
      <tr>
        <td id="L454" class="blob-num js-line-number" data-line-number="454"></td>
        <td id="LC454" class="blob-code js-file-line">            mcmc.use_step_method(pymc.Metropolis, <span class="pl-v">self</span>.P0)</td>
      </tr>
      <tr>
        <td id="L455" class="blob-num js-line-number" data-line-number="455"></td>
        <td id="LC455" class="blob-code js-file-line">        <span class="pl-k">if</span> Ls_stated <span class="pl-k">&gt;</span> Quantity(<span class="pl-s"><span class="pl-pds">&#39;</span>0.0 molar<span class="pl-pds">&#39;</span></span>):</td>
      </tr>
      <tr>
        <td id="L456" class="blob-num js-line-number" data-line-number="456"></td>
        <td id="LC456" class="blob-code js-file-line">            mcmc.use_step_method(pymc.Metropolis, <span class="pl-v">self</span>.Ls)</td>
      </tr>
      <tr>
        <td id="L457" class="blob-num js-line-number" data-line-number="457"></td>
        <td id="LC457" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L458" class="blob-num js-line-number" data-line-number="458"></td>
        <td id="LC458" class="blob-code js-file-line">        <span class="pl-k">return</span> mcmc</td>
      </tr>
      <tr>
        <td id="L459" class="blob-num js-line-number" data-line-number="459"></td>
        <td id="LC459" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L460" class="blob-num js-line-number" data-line-number="460"></td>
        <td id="LC460" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L461" class="blob-num js-line-number" data-line-number="461"></td>
        <td id="LC461" class="blob-code js-file-line">    <span class="pl-k">def</span> <span class="pl-en">_lambda_heats_model</span>(<span class="pl-smi">self</span>, <span class="pl-smi">q_name</span><span class="pl-k">=</span><span class="pl-s"><span class="pl-pds">&#39;</span>q_n_model<span class="pl-pds">&#39;</span></span>):</td>
      </tr>
      <tr>
        <td id="L462" class="blob-num js-line-number" data-line-number="462"></td>
        <td id="LC462" class="blob-code js-file-line">        <span class="pl-s"><span class="pl-pds">&quot;&quot;&quot;</span>Model the heat using expected_injection_heats, providing all input by using a lambda function</span></td>
      </tr>
      <tr>
        <td id="L463" class="blob-num js-line-number" data-line-number="463"></td>
        <td id="LC463" class="blob-code js-file-line"><span class="pl-s">            q_name is the name for the model</span></td>
      </tr>
      <tr>
        <td id="L464" class="blob-num js-line-number" data-line-number="464"></td>
        <td id="LC464" class="blob-code js-file-line"><span class="pl-s">        <span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L465" class="blob-num js-line-number" data-line-number="465"></td>
        <td id="LC465" class="blob-code js-file-line">        <span class="pl-k">return</span> pymc.Lambda(q_name,</td>
      </tr>
      <tr>
        <td id="L466" class="blob-num js-line-number" data-line-number="466"></td>
        <td id="LC466" class="blob-code js-file-line">                           <span class="pl-k">lambda</span></td>
      </tr>
      <tr>
        <td id="L467" class="blob-num js-line-number" data-line-number="467"></td>
        <td id="LC467" class="blob-code js-file-line">                               <span class="pl-smi">P0</span><span class="pl-k">=</span><span class="pl-v">self</span>.P0,</td>
      </tr>
      <tr>
        <td id="L468" class="blob-num js-line-number" data-line-number="468"></td>
        <td id="LC468" class="blob-code js-file-line">                               <span class="pl-smi">Ls</span><span class="pl-k">=</span><span class="pl-v">self</span>.Ls,</td>
      </tr>
      <tr>
        <td id="L469" class="blob-num js-line-number" data-line-number="469"></td>
        <td id="LC469" class="blob-code js-file-line">                               <span class="pl-smi">DeltaG</span><span class="pl-k">=</span><span class="pl-v">self</span>.DeltaG,</td>
      </tr>
      <tr>
        <td id="L470" class="blob-num js-line-number" data-line-number="470"></td>
        <td id="LC470" class="blob-code js-file-line">                               <span class="pl-smi">DeltaH</span><span class="pl-k">=</span><span class="pl-v">self</span>.DeltaH,</td>
      </tr>
      <tr>
        <td id="L471" class="blob-num js-line-number" data-line-number="471"></td>
        <td id="LC471" class="blob-code js-file-line">                               <span class="pl-smi">DeltaH_0</span><span class="pl-k">=</span><span class="pl-v">self</span>.DeltaH_0:</td>
      </tr>
      <tr>
        <td id="L472" class="blob-num js-line-number" data-line-number="472"></td>
        <td id="LC472" class="blob-code js-file-line">                           <span class="pl-v">self</span>.expected_injection_heats(</td>
      </tr>
      <tr>
        <td id="L473" class="blob-num js-line-number" data-line-number="473"></td>
        <td id="LC473" class="blob-code js-file-line">                               <span class="pl-v">self</span>.V0,</td>
      </tr>
      <tr>
        <td id="L474" class="blob-num js-line-number" data-line-number="474"></td>
        <td id="LC474" class="blob-code js-file-line">                               <span class="pl-v">self</span>.DeltaVn,</td>
      </tr>
      <tr>
        <td id="L475" class="blob-num js-line-number" data-line-number="475"></td>
        <td id="LC475" class="blob-code js-file-line">                               P0,</td>
      </tr>
      <tr>
        <td id="L476" class="blob-num js-line-number" data-line-number="476"></td>
        <td id="LC476" class="blob-code js-file-line">                               Ls,</td>
      </tr>
      <tr>
        <td id="L477" class="blob-num js-line-number" data-line-number="477"></td>
        <td id="LC477" class="blob-code js-file-line">                               DeltaG,</td>
      </tr>
      <tr>
        <td id="L478" class="blob-num js-line-number" data-line-number="478"></td>
        <td id="LC478" class="blob-code js-file-line">                               DeltaH,</td>
      </tr>
      <tr>
        <td id="L479" class="blob-num js-line-number" data-line-number="479"></td>
        <td id="LC479" class="blob-code js-file-line">                               DeltaH_0,</td>
      </tr>
      <tr>
        <td id="L480" class="blob-num js-line-number" data-line-number="480"></td>
        <td id="LC480" class="blob-code js-file-line">                               <span class="pl-v">self</span>.beta,</td>
      </tr>
      <tr>
        <td id="L481" class="blob-num js-line-number" data-line-number="481"></td>
        <td id="LC481" class="blob-code js-file-line">                               <span class="pl-v">self</span>.N</td>
      </tr>
      <tr>
        <td id="L482" class="blob-num js-line-number" data-line-number="482"></td>
        <td id="LC482" class="blob-code js-file-line">                           )</td>
      </tr>
      <tr>
        <td id="L483" class="blob-num js-line-number" data-line-number="483"></td>
        <td id="LC483" class="blob-code js-file-line">        )</td>
      </tr>
      <tr>
        <td id="L484" class="blob-num js-line-number" data-line-number="484"></td>
        <td id="LC484" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L485" class="blob-num js-line-number" data-line-number="485"></td>
        <td id="LC485" class="blob-code js-file-line">    <span class="pl-k">def</span> <span class="pl-en">_lambda_tau_model</span>(<span class="pl-smi">self</span>):</td>
      </tr>
      <tr>
        <td id="L486" class="blob-num js-line-number" data-line-number="486"></td>
        <td id="LC486" class="blob-code js-file-line">        <span class="pl-s"><span class="pl-pds">&quot;&quot;&quot;</span>Model for tau implemented using lambda function<span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L487" class="blob-num js-line-number" data-line-number="487"></td>
        <td id="LC487" class="blob-code js-file-line">        <span class="pl-k">return</span> pymc.Lambda(<span class="pl-s"><span class="pl-pds">&#39;</span>tau<span class="pl-pds">&#39;</span></span>, <span class="pl-k">lambda</span> <span class="pl-smi">log_sigma</span><span class="pl-k">=</span><span class="pl-v">self</span>.log_sigma: <span class="pl-v">self</span>.tau(log_sigma))</td>
      </tr>
      <tr>
        <td id="L488" class="blob-num js-line-number" data-line-number="488"></td>
        <td id="LC488" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L489" class="blob-num js-line-number" data-line-number="489"></td>
        <td id="LC489" class="blob-code js-file-line">    <span class="pl-en">@<span class="pl-c1">staticmethod</span></span></td>
      </tr>
      <tr>
        <td id="L490" class="blob-num js-line-number" data-line-number="490"></td>
        <td id="LC490" class="blob-code js-file-line">    <span class="pl-k">def</span> <span class="pl-en">_logsigma_guesses</span>(<span class="pl-smi">q_n</span>, <span class="pl-smi">number_of_inj</span>, <span class="pl-smi">standard_unit</span>):</td>
      </tr>
      <tr>
        <td id="L491" class="blob-num js-line-number" data-line-number="491"></td>
        <td id="LC491" class="blob-code js-file-line">        <span class="pl-s"><span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L492" class="blob-num js-line-number" data-line-number="492"></td>
        <td id="LC492" class="blob-code js-file-line"><span class="pl-s">        q_n: list/array of heats</span></td>
      </tr>
      <tr>
        <td id="L493" class="blob-num js-line-number" data-line-number="493"></td>
        <td id="LC493" class="blob-code js-file-line"><span class="pl-s">        number_of_inj: number of injections at end of protocol to use for estimating sigma</span></td>
      </tr>
      <tr>
        <td id="L494" class="blob-num js-line-number" data-line-number="494"></td>
        <td id="LC494" class="blob-code js-file-line"><span class="pl-s">        standard_unit: unit by which to correct the magnitude of sigma</span></td>
      </tr>
      <tr>
        <td id="L495" class="blob-num js-line-number" data-line-number="495"></td>
        <td id="LC495" class="blob-code js-file-line"><span class="pl-s">        <span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L496" class="blob-num js-line-number" data-line-number="496"></td>
        <td id="LC496" class="blob-code js-file-line">        <span class="pl-c"># review: how can we do this better?</span></td>
      </tr>
      <tr>
        <td id="L497" class="blob-num js-line-number" data-line-number="497"></td>
        <td id="LC497" class="blob-code js-file-line">        log_sigma_guess <span class="pl-k">=</span> log(q_n[<span class="pl-k">-</span>number_of_inj:].std() <span class="pl-k">/</span> standard_unit)</td>
      </tr>
      <tr>
        <td id="L498" class="blob-num js-line-number" data-line-number="498"></td>
        <td id="LC498" class="blob-code js-file-line">        log_sigma_min <span class="pl-k">=</span> log_sigma_guess <span class="pl-k">-</span> <span class="pl-c1">10</span></td>
      </tr>
      <tr>
        <td id="L499" class="blob-num js-line-number" data-line-number="499"></td>
        <td id="LC499" class="blob-code js-file-line">        log_sigma_max <span class="pl-k">=</span> log_sigma_guess <span class="pl-k">+</span> <span class="pl-c1">5</span></td>
      </tr>
      <tr>
        <td id="L500" class="blob-num js-line-number" data-line-number="500"></td>
        <td id="LC500" class="blob-code js-file-line">        <span class="pl-k">return</span> log_sigma_guess, log_sigma_max, log_sigma_min</td>
      </tr>
      <tr>
        <td id="L501" class="blob-num js-line-number" data-line-number="501"></td>
        <td id="LC501" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L502" class="blob-num js-line-number" data-line-number="502"></td>
        <td id="LC502" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L503" class="blob-num js-line-number" data-line-number="503"></td>
        <td id="LC503" class="blob-code js-file-line"><span class="pl-k">class</span> <span class="pl-en">CompetitiveBindingModel</span>(<span class="pl-e">BindingModel</span>):</td>
      </tr>
      <tr>
        <td id="L504" class="blob-num js-line-number" data-line-number="504"></td>
        <td id="LC504" class="blob-code js-file-line">    <span class="pl-s"><span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L505" class="blob-num js-line-number" data-line-number="505"></td>
        <td id="LC505" class="blob-code js-file-line"><span class="pl-s">    Competitive binding model.</span></td>
      </tr>
      <tr>
        <td id="L506" class="blob-num js-line-number" data-line-number="506"></td>
        <td id="LC506" class="blob-code js-file-line"><span class="pl-s">    <span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L507" class="blob-num js-line-number" data-line-number="507"></td>
        <td id="LC507" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L508" class="blob-num js-line-number" data-line-number="508"></td>
        <td id="LC508" class="blob-code js-file-line">    <span class="pl-k">def</span> <span class="pl-en"><span class="pl-c1">__init__</span></span>(<span class="pl-smi">self</span>, <span class="pl-smi">experiments</span>, <span class="pl-smi">receptor</span>, <span class="pl-smi">concentration_uncertainty</span><span class="pl-k">=</span><span class="pl-c1">0.10</span>):</td>
      </tr>
      <tr>
        <td id="L509" class="blob-num js-line-number" data-line-number="509"></td>
        <td id="LC509" class="blob-code js-file-line">        <span class="pl-s"><span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L510" class="blob-num js-line-number" data-line-number="510"></td>
        <td id="LC510" class="blob-code js-file-line"><span class="pl-s">        ARGUMENTS</span></td>
      </tr>
      <tr>
        <td id="L511" class="blob-num js-line-number" data-line-number="511"></td>
        <td id="LC511" class="blob-code js-file-line"><span class="pl-s">        experiments (list of Experiment) -</span></td>
      </tr>
      <tr>
        <td id="L512" class="blob-num js-line-number" data-line-number="512"></td>
        <td id="LC512" class="blob-code js-file-line"><span class="pl-s">        instrument Instrument that experiment was carried out in (has to be one)</span></td>
      </tr>
      <tr>
        <td id="L513" class="blob-num js-line-number" data-line-number="513"></td>
        <td id="LC513" class="blob-code js-file-line"><span class="pl-s">        receptor (string) - name of receptor species</span></td>
      </tr>
      <tr>
        <td id="L514" class="blob-num js-line-number" data-line-number="514"></td>
        <td id="LC514" class="blob-code js-file-line"><span class="pl-s">        OPTIONAL ARGUMENTS</span></td>
      </tr>
      <tr>
        <td id="L515" class="blob-num js-line-number" data-line-number="515"></td>
        <td id="LC515" class="blob-code js-file-line"><span class="pl-s">        concentration_uncertainty (float) - relative uncertainty in concentrations</span></td>
      </tr>
      <tr>
        <td id="L516" class="blob-num js-line-number" data-line-number="516"></td>
        <td id="LC516" class="blob-code js-file-line"><span class="pl-s">        <span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L517" class="blob-num js-line-number" data-line-number="517"></td>
        <td id="LC517" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L518" class="blob-num js-line-number" data-line-number="518"></td>
        <td id="LC518" class="blob-code js-file-line">        <span class="pl-c"># Store temperature.</span></td>
      </tr>
      <tr>
        <td id="L519" class="blob-num js-line-number" data-line-number="519"></td>
        <td id="LC519" class="blob-code js-file-line">        <span class="pl-c"># NOTE: Right now, there can only be one.</span></td>
      </tr>
      <tr>
        <td id="L520" class="blob-num js-line-number" data-line-number="520"></td>
        <td id="LC520" class="blob-code js-file-line">        <span class="pl-v">self</span>.temperature <span class="pl-k">=</span> experiments[<span class="pl-c1">0</span>].temperature  <span class="pl-c"># temperature (kelvin)</span></td>
      </tr>
      <tr>
        <td id="L521" class="blob-num js-line-number" data-line-number="521"></td>
        <td id="LC521" class="blob-code js-file-line">        <span class="pl-c"># inverse temperature 1/(kcal/mol)</span></td>
      </tr>
      <tr>
        <td id="L522" class="blob-num js-line-number" data-line-number="522"></td>
        <td id="LC522" class="blob-code js-file-line">        <span class="pl-v">self</span>.beta <span class="pl-k">=</span> <span class="pl-c1">1.0</span> <span class="pl-k">/</span> (ureg.molar_gas_constant <span class="pl-k">*</span> <span class="pl-v">self</span>.temperature)</td>
      </tr>
      <tr>
        <td id="L523" class="blob-num js-line-number" data-line-number="523"></td>
        <td id="LC523" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L524" class="blob-num js-line-number" data-line-number="524"></td>
        <td id="LC524" class="blob-code js-file-line">        <span class="pl-c"># Store copy of experiments.</span></td>
      </tr>
      <tr>
        <td id="L525" class="blob-num js-line-number" data-line-number="525"></td>
        <td id="LC525" class="blob-code js-file-line">        <span class="pl-v">self</span>.experiments <span class="pl-k">=</span> experiments</td>
      </tr>
      <tr>
        <td id="L526" class="blob-num js-line-number" data-line-number="526"></td>
        <td id="LC526" class="blob-code js-file-line">        logging.info(<span class="pl-s"><span class="pl-pds">&quot;</span><span class="pl-c1">%d</span> experiments<span class="pl-pds">&quot;</span></span> <span class="pl-k">%</span> <span class="pl-c1">len</span>(<span class="pl-v">self</span>.experiments))</td>
      </tr>
      <tr>
        <td id="L527" class="blob-num js-line-number" data-line-number="527"></td>
        <td id="LC527" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L528" class="blob-num js-line-number" data-line-number="528"></td>
        <td id="LC528" class="blob-code js-file-line">        <span class="pl-c"># Store sample cell volume.</span></td>
      </tr>
      <tr>
        <td id="L529" class="blob-num js-line-number" data-line-number="529"></td>
        <td id="LC529" class="blob-code js-file-line">        <span class="pl-v">self</span>.V0 <span class="pl-k">=</span> <span class="pl-v">self</span>.experiments[<span class="pl-c1">0</span>].cell_volume</td>
      </tr>
      <tr>
        <td id="L530" class="blob-num js-line-number" data-line-number="530"></td>
        <td id="LC530" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L531" class="blob-num js-line-number" data-line-number="531"></td>
        <td id="LC531" class="blob-code js-file-line">        <span class="pl-c"># Store the name of the receptor.</span></td>
      </tr>
      <tr>
        <td id="L532" class="blob-num js-line-number" data-line-number="532"></td>
        <td id="LC532" class="blob-code js-file-line">        <span class="pl-v">self</span>.receptor <span class="pl-k">=</span> receptor</td>
      </tr>
      <tr>
        <td id="L533" class="blob-num js-line-number" data-line-number="533"></td>
        <td id="LC533" class="blob-code js-file-line">        logging.info(<span class="pl-s"><span class="pl-pds">&quot;</span>species &#39;<span class="pl-c1">%s</span>&#39; will be treated as receptor<span class="pl-pds">&quot;</span></span> <span class="pl-k">%</span> <span class="pl-v">self</span>.receptor)</td>
      </tr>
      <tr>
        <td id="L534" class="blob-num js-line-number" data-line-number="534"></td>
        <td id="LC534" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L535" class="blob-num js-line-number" data-line-number="535"></td>
        <td id="LC535" class="blob-code js-file-line">        <span class="pl-c"># Make a list of names of all molecular species.</span></td>
      </tr>
      <tr>
        <td id="L536" class="blob-num js-line-number" data-line-number="536"></td>
        <td id="LC536" class="blob-code js-file-line">        <span class="pl-v">self</span>.species <span class="pl-k">=</span> <span class="pl-v">self</span>._species_from_experiments(experiments)</td>
      </tr>
      <tr>
        <td id="L537" class="blob-num js-line-number" data-line-number="537"></td>
        <td id="LC537" class="blob-code js-file-line">        logging.info(<span class="pl-s"><span class="pl-pds">&quot;</span>species: <span class="pl-c1">%s</span><span class="pl-pds">&quot;</span></span> <span class="pl-k">%</span> <span class="pl-v">self</span>.species)</td>
      </tr>
      <tr>
        <td id="L538" class="blob-num js-line-number" data-line-number="538"></td>
        <td id="LC538" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L539" class="blob-num js-line-number" data-line-number="539"></td>
        <td id="LC539" class="blob-code js-file-line">        <span class="pl-c"># Make a list of all ligands.</span></td>
      </tr>
      <tr>
        <td id="L540" class="blob-num js-line-number" data-line-number="540"></td>
        <td id="LC540" class="blob-code js-file-line">        <span class="pl-v">self</span>.ligands <span class="pl-k">=</span> copy.deepcopy(<span class="pl-v">self</span>.species)</td>
      </tr>
      <tr>
        <td id="L541" class="blob-num js-line-number" data-line-number="541"></td>
        <td id="LC541" class="blob-code js-file-line">        <span class="pl-v">self</span>.ligands.remove(receptor)</td>
      </tr>
      <tr>
        <td id="L542" class="blob-num js-line-number" data-line-number="542"></td>
        <td id="LC542" class="blob-code js-file-line">        logging.info(<span class="pl-s"><span class="pl-pds">&quot;</span>ligands: <span class="pl-c1">%s</span><span class="pl-pds">&quot;</span></span> <span class="pl-k">%</span> <span class="pl-v">self</span>.ligands)</td>
      </tr>
      <tr>
        <td id="L543" class="blob-num js-line-number" data-line-number="543"></td>
        <td id="LC543" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L544" class="blob-num js-line-number" data-line-number="544"></td>
        <td id="LC544" class="blob-code js-file-line">        <span class="pl-c"># Create a list of all stochastics.</span></td>
      </tr>
      <tr>
        <td id="L545" class="blob-num js-line-number" data-line-number="545"></td>
        <td id="LC545" class="blob-code js-file-line">        <span class="pl-v">self</span>.stochastics <span class="pl-k">=</span> <span class="pl-c1">list</span>()</td>
      </tr>
      <tr>
        <td id="L546" class="blob-num js-line-number" data-line-number="546"></td>
        <td id="LC546" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L547" class="blob-num js-line-number" data-line-number="547"></td>
        <td id="LC547" class="blob-code js-file-line">        <span class="pl-c"># Create a prior for thermodynamic parameters of binding for each ligand-receptor interaction.</span></td>
      </tr>
      <tr>
        <td id="L548" class="blob-num js-line-number" data-line-number="548"></td>
        <td id="LC548" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L549" class="blob-num js-line-number" data-line-number="549"></td>
        <td id="LC549" class="blob-code js-file-line">        <span class="pl-v">self</span>.thermodynamic_parameters <span class="pl-k">=</span> <span class="pl-c1">dict</span>()</td>
      </tr>
      <tr>
        <td id="L550" class="blob-num js-line-number" data-line-number="550"></td>
        <td id="LC550" class="blob-code js-file-line">        <span class="pl-c"># TODO: add option to set initial thermodynamic parameters to literature values.</span></td>
      </tr>
      <tr>
        <td id="L551" class="blob-num js-line-number" data-line-number="551"></td>
        <td id="LC551" class="blob-code js-file-line">        <span class="pl-k">for</span> ligand <span class="pl-k">in</span> <span class="pl-v">self</span>.ligands:</td>
      </tr>
      <tr>
        <td id="L552" class="blob-num js-line-number" data-line-number="552"></td>
        <td id="LC552" class="blob-code js-file-line">            <span class="pl-c"># define the name and prior for each receptor ligand combination</span></td>
      </tr>
      <tr>
        <td id="L553" class="blob-num js-line-number" data-line-number="553"></td>
        <td id="LC553" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L554" class="blob-num js-line-number" data-line-number="554"></td>
        <td id="LC554" class="blob-code js-file-line">            <span class="pl-c"># delta G of binding</span></td>
      </tr>
      <tr>
        <td id="L555" class="blob-num js-line-number" data-line-number="555"></td>
        <td id="LC555" class="blob-code js-file-line">            dg_name <span class="pl-k">=</span> <span class="pl-s"><span class="pl-pds">&quot;</span>DeltaG of <span class="pl-c1">%s</span> * <span class="pl-c1">%s</span><span class="pl-pds">&quot;</span></span> <span class="pl-k">%</span> (<span class="pl-v">self</span>.receptor, ligand)</td>
      </tr>
      <tr>
        <td id="L556" class="blob-num js-line-number" data-line-number="556"></td>
        <td id="LC556" class="blob-code js-file-line">            prior_deltag <span class="pl-k">=</span> BindingModel._uniform_prior_with_guesses_and_units(dg_name, <span class="pl-c1">0.</span>, <span class="pl-c1">40.</span>, <span class="pl-k">-</span><span class="pl-c1">40.</span>, ureg.kilocalorie <span class="pl-k">/</span> ureg.mole)</td>
      </tr>
      <tr>
        <td id="L557" class="blob-num js-line-number" data-line-number="557"></td>
        <td id="LC557" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L558" class="blob-num js-line-number" data-line-number="558"></td>
        <td id="LC558" class="blob-code js-file-line">            <span class="pl-c"># delta H of binding</span></td>
      </tr>
      <tr>
        <td id="L559" class="blob-num js-line-number" data-line-number="559"></td>
        <td id="LC559" class="blob-code js-file-line">            dh_name <span class="pl-k">=</span> <span class="pl-s"><span class="pl-pds">&quot;</span>DeltaH of <span class="pl-c1">%s</span> * <span class="pl-c1">%s</span><span class="pl-pds">&quot;</span></span> <span class="pl-k">%</span> (<span class="pl-v">self</span>.receptor, ligand)</td>
      </tr>
      <tr>
        <td id="L560" class="blob-num js-line-number" data-line-number="560"></td>
        <td id="LC560" class="blob-code js-file-line">            prior_deltah <span class="pl-k">=</span> BindingModel._uniform_prior_with_guesses_and_units(dh_name, <span class="pl-c1">0.</span>, <span class="pl-c1">100.</span>, <span class="pl-k">-</span><span class="pl-c1">100.</span>, ureg.kilocalorie <span class="pl-k">/</span> ureg.mole)</td>
      </tr>
      <tr>
        <td id="L561" class="blob-num js-line-number" data-line-number="561"></td>
        <td id="LC561" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L562" class="blob-num js-line-number" data-line-number="562"></td>
        <td id="LC562" class="blob-code js-file-line">            <span class="pl-v">self</span>.thermodynamic_parameters[dg_name] <span class="pl-k">=</span> prior_deltag</td>
      </tr>
      <tr>
        <td id="L563" class="blob-num js-line-number" data-line-number="563"></td>
        <td id="LC563" class="blob-code js-file-line">            <span class="pl-v">self</span>.thermodynamic_parameters[dh_name] <span class="pl-k">=</span> prior_deltah</td>
      </tr>
      <tr>
        <td id="L564" class="blob-num js-line-number" data-line-number="564"></td>
        <td id="LC564" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L565" class="blob-num js-line-number" data-line-number="565"></td>
        <td id="LC565" class="blob-code js-file-line">            <span class="pl-v">self</span>.stochastics.append(prior_deltag)</td>
      </tr>
      <tr>
        <td id="L566" class="blob-num js-line-number" data-line-number="566"></td>
        <td id="LC566" class="blob-code js-file-line">            <span class="pl-v">self</span>.stochastics.append(prior_deltah)</td>
      </tr>
      <tr>
        <td id="L567" class="blob-num js-line-number" data-line-number="567"></td>
        <td id="LC567" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L568" class="blob-num js-line-number" data-line-number="568"></td>
        <td id="LC568" class="blob-code js-file-line">        logging.debug(<span class="pl-s"><span class="pl-pds">&quot;</span>thermodynamic parameters:<span class="pl-pds">&quot;</span></span>)</td>
      </tr>
      <tr>
        <td id="L569" class="blob-num js-line-number" data-line-number="569"></td>
        <td id="LC569" class="blob-code js-file-line">        logging.debug(<span class="pl-v">self</span>.thermodynamic_parameters)</td>
      </tr>
      <tr>
        <td id="L570" class="blob-num js-line-number" data-line-number="570"></td>
        <td id="LC570" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L571" class="blob-num js-line-number" data-line-number="571"></td>
        <td id="LC571" class="blob-code js-file-line">        log_sigma_guess, log_sigma_max, log_sigma_min <span class="pl-k">=</span> <span class="pl-v">self</span>._logsigma_guesses_from_multiple_experiments(ureg.calorie)</td>
      </tr>
      <tr>
        <td id="L572" class="blob-num js-line-number" data-line-number="572"></td>
        <td id="LC572" class="blob-code js-file-line">        <span class="pl-v">self</span>.log_sigma <span class="pl-k">=</span> BindingModel._uniform_prior(<span class="pl-s"><span class="pl-pds">&#39;</span>log_sigma<span class="pl-pds">&#39;</span></span>, log_sigma_guess, log_sigma_max, log_sigma_min)</td>
      </tr>
      <tr>
        <td id="L573" class="blob-num js-line-number" data-line-number="573"></td>
        <td id="LC573" class="blob-code js-file-line">        <span class="pl-v">self</span>.stochastics.append(<span class="pl-v">self</span>.log_sigma)</td>
      </tr>
      <tr>
        <td id="L574" class="blob-num js-line-number" data-line-number="574"></td>
        <td id="LC574" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L575" class="blob-num js-line-number" data-line-number="575"></td>
        <td id="LC575" class="blob-code js-file-line">        tau <span class="pl-k">=</span> pymc.Lambda(<span class="pl-s"><span class="pl-pds">&#39;</span>tau<span class="pl-pds">&#39;</span></span>, <span class="pl-k">lambda</span> <span class="pl-smi">log_sigma</span><span class="pl-k">=</span><span class="pl-v">self</span>.log_sigma: exp(<span class="pl-k">-</span><span class="pl-c1">2.0</span> <span class="pl-k">*</span> log_sigma))</td>
      </tr>
      <tr>
        <td id="L576" class="blob-num js-line-number" data-line-number="576"></td>
        <td id="LC576" class="blob-code js-file-line">        <span class="pl-v">self</span>.stochastics.append(tau)</td>
      </tr>
      <tr>
        <td id="L577" class="blob-num js-line-number" data-line-number="577"></td>
        <td id="LC577" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L578" class="blob-num js-line-number" data-line-number="578"></td>
        <td id="LC578" class="blob-code js-file-line">        <span class="pl-c"># Define priors for unknowns for each experiment.</span></td>
      </tr>
      <tr>
        <td id="L579" class="blob-num js-line-number" data-line-number="579"></td>
        <td id="LC579" class="blob-code js-file-line">        <span class="pl-k">for</span> (index, experiment) <span class="pl-k">in</span> <span class="pl-c1">enumerate</span>(<span class="pl-v">self</span>.experiments):</td>
      </tr>
      <tr>
        <td id="L580" class="blob-num js-line-number" data-line-number="580"></td>
        <td id="LC580" class="blob-code js-file-line">            <span class="pl-c"># Number of observations</span></td>
      </tr>
      <tr>
        <td id="L581" class="blob-num js-line-number" data-line-number="581"></td>
        <td id="LC581" class="blob-code js-file-line">            experiment.ninjections <span class="pl-k">=</span> experiment.observed_injection_heats.size</td>
      </tr>
      <tr>
        <td id="L582" class="blob-num js-line-number" data-line-number="582"></td>
        <td id="LC582" class="blob-code js-file-line">            logging.info(<span class="pl-s"><span class="pl-pds">&quot;</span>Experiment <span class="pl-c1">%d</span> has <span class="pl-c1">%d</span> injections<span class="pl-pds">&quot;</span></span> <span class="pl-k">%</span></td>
      </tr>
      <tr>
        <td id="L583" class="blob-num js-line-number" data-line-number="583"></td>
        <td id="LC583" class="blob-code js-file-line">                         (index, experiment.ninjections))</td>
      </tr>
      <tr>
        <td id="L584" class="blob-num js-line-number" data-line-number="584"></td>
        <td id="LC584" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L585" class="blob-num js-line-number" data-line-number="585"></td>
        <td id="LC585" class="blob-code js-file-line">            dh0_name <span class="pl-k">=</span> <span class="pl-s"><span class="pl-pds">&quot;</span>DeltaH_0 for experiment <span class="pl-c1">%d</span><span class="pl-pds">&quot;</span></span> <span class="pl-k">%</span> index</td>
      </tr>
      <tr>
        <td id="L586" class="blob-num js-line-number" data-line-number="586"></td>
        <td id="LC586" class="blob-code js-file-line">            experiment.DeltaH_0 <span class="pl-k">=</span> BindingModel._uniform_prior_with_guesses_and_units(dh0_name, <span class="pl-k">*</span><span class="pl-v">self</span>._deltaH0_guesses(experiment.observed_injection_heats), <span class="pl-smi">prior_unit</span><span class="pl-k">=</span>ureg.calorie, <span class="pl-smi">guess_unit</span><span class="pl-k">=</span><span class="pl-c1">True</span>)</td>
      </tr>
      <tr>
        <td id="L587" class="blob-num js-line-number" data-line-number="587"></td>
        <td id="LC587" class="blob-code js-file-line">            <span class="pl-v">self</span>.stochastics.append(experiment.DeltaH_0)</td>
      </tr>
      <tr>
        <td id="L588" class="blob-num js-line-number" data-line-number="588"></td>
        <td id="LC588" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L589" class="blob-num js-line-number" data-line-number="589"></td>
        <td id="LC589" class="blob-code js-file-line">            <span class="pl-c"># Define priors for the true concentration of each component</span></td>
      </tr>
      <tr>
        <td id="L590" class="blob-num js-line-number" data-line-number="590"></td>
        <td id="LC590" class="blob-code js-file-line">            experiment.true_cell_concentration <span class="pl-k">=</span> <span class="pl-c1">dict</span>()</td>
      </tr>
      <tr>
        <td id="L591" class="blob-num js-line-number" data-line-number="591"></td>
        <td id="LC591" class="blob-code js-file-line">            <span class="pl-k">for</span> species, concentration <span class="pl-k">in</span> experiment.cell_concentration.iteritems():</td>
      </tr>
      <tr>
        <td id="L592" class="blob-num js-line-number" data-line-number="592"></td>
        <td id="LC592" class="blob-code js-file-line">                name <span class="pl-k">=</span> <span class="pl-s"><span class="pl-pds">&quot;</span>initial sample cell concentration of <span class="pl-c1">%s</span> in experiment <span class="pl-c1">%d</span><span class="pl-pds">&quot;</span></span> <span class="pl-k">%</span> (species, index)</td>
      </tr>
      <tr>
        <td id="L593" class="blob-num js-line-number" data-line-number="593"></td>
        <td id="LC593" class="blob-code js-file-line">                cell_concentration_prior <span class="pl-k">=</span> BindingModel._lognormal_concentration_prior(name, concentration, concentration_uncertainty <span class="pl-k">*</span> concentration, ureg.millimole <span class="pl-k">/</span> ureg.liter)</td>
      </tr>
      <tr>
        <td id="L594" class="blob-num js-line-number" data-line-number="594"></td>
        <td id="LC594" class="blob-code js-file-line">                experiment.true_cell_concentration[species] <span class="pl-k">=</span> cell_concentration_prior</td>
      </tr>
      <tr>
        <td id="L595" class="blob-num js-line-number" data-line-number="595"></td>
        <td id="LC595" class="blob-code js-file-line">                <span class="pl-v">self</span>.stochastics.append(cell_concentration_prior)</td>
      </tr>
      <tr>
        <td id="L596" class="blob-num js-line-number" data-line-number="596"></td>
        <td id="LC596" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L597" class="blob-num js-line-number" data-line-number="597"></td>
        <td id="LC597" class="blob-code js-file-line">            experiment.true_syringe_concentration <span class="pl-k">=</span> <span class="pl-c1">dict</span>()</td>
      </tr>
      <tr>
        <td id="L598" class="blob-num js-line-number" data-line-number="598"></td>
        <td id="LC598" class="blob-code js-file-line">            <span class="pl-k">for</span> species, concentration <span class="pl-k">in</span> experiment.syringe_concentration.iteritems():</td>
      </tr>
      <tr>
        <td id="L599" class="blob-num js-line-number" data-line-number="599"></td>
        <td id="LC599" class="blob-code js-file-line">                name <span class="pl-k">=</span> <span class="pl-s"><span class="pl-pds">&quot;</span>initial syringe concentration of <span class="pl-c1">%s</span> in experiment <span class="pl-c1">%d</span><span class="pl-pds">&quot;</span></span> <span class="pl-k">%</span> (species, index)</td>
      </tr>
      <tr>
        <td id="L600" class="blob-num js-line-number" data-line-number="600"></td>
        <td id="LC600" class="blob-code js-file-line">                syringe_concentration_prior <span class="pl-k">=</span> BindingModel._lognormal_concentration_prior(name, concentration, concentration_uncertainty <span class="pl-k">*</span> concentration, ureg.millimole <span class="pl-k">/</span> ureg.liter)</td>
      </tr>
      <tr>
        <td id="L601" class="blob-num js-line-number" data-line-number="601"></td>
        <td id="LC601" class="blob-code js-file-line">                experiment.true_cell_concentration[species] <span class="pl-k">=</span> syringe_concentration_prior</td>
      </tr>
      <tr>
        <td id="L602" class="blob-num js-line-number" data-line-number="602"></td>
        <td id="LC602" class="blob-code js-file-line">                <span class="pl-v">self</span>.stochastics.append(syringe_concentration_prior)</td>
      </tr>
      <tr>
        <td id="L603" class="blob-num js-line-number" data-line-number="603"></td>
        <td id="LC603" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L604" class="blob-num js-line-number" data-line-number="604"></td>
        <td id="LC604" class="blob-code js-file-line">            <span class="pl-c"># Add species not explicitly listed with zero concentration.</span></td>
      </tr>
      <tr>
        <td id="L605" class="blob-num js-line-number" data-line-number="605"></td>
        <td id="LC605" class="blob-code js-file-line">            <span class="pl-v">self</span>._zero_for_missing__concentrations(experiment)</td>
      </tr>
      <tr>
        <td id="L606" class="blob-num js-line-number" data-line-number="606"></td>
        <td id="LC606" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L607" class="blob-num js-line-number" data-line-number="607"></td>
        <td id="LC607" class="blob-code js-file-line">            <span class="pl-c"># True injection heats</span></td>
      </tr>
      <tr>
        <td id="L608" class="blob-num js-line-number" data-line-number="608"></td>
        <td id="LC608" class="blob-code js-file-line">            q_name <span class="pl-k">=</span> <span class="pl-s"><span class="pl-pds">&quot;</span>true injection heats for experiment <span class="pl-c1">%d</span><span class="pl-pds">&quot;</span></span> <span class="pl-k">%</span> index</td>
      </tr>
      <tr>
        <td id="L609" class="blob-num js-line-number" data-line-number="609"></td>
        <td id="LC609" class="blob-code js-file-line">            experiment.true_injection_heats <span class="pl-k">=</span> <span class="pl-v">self</span>._lambda_heats_model(experiment, q_name)</td>
      </tr>
      <tr>
        <td id="L610" class="blob-num js-line-number" data-line-number="610"></td>
        <td id="LC610" class="blob-code js-file-line">            <span class="pl-v">self</span>.stochastics.append(experiment.true_injection_heats)</td>
      </tr>
      <tr>
        <td id="L611" class="blob-num js-line-number" data-line-number="611"></td>
        <td id="LC611" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L612" class="blob-num js-line-number" data-line-number="612"></td>
        <td id="LC612" class="blob-code js-file-line">            <span class="pl-c"># Observed injection heats</span></td>
      </tr>
      <tr>
        <td id="L613" class="blob-num js-line-number" data-line-number="613"></td>
        <td id="LC613" class="blob-code js-file-line">            q_n_obs_name <span class="pl-k">=</span> <span class="pl-s"><span class="pl-pds">&quot;</span>observed injection heats for experiment <span class="pl-c1">%d</span><span class="pl-pds">&quot;</span></span> <span class="pl-k">%</span> index</td>
      </tr>
      <tr>
        <td id="L614" class="blob-num js-line-number" data-line-number="614"></td>
        <td id="LC614" class="blob-code js-file-line">            experiment.observation <span class="pl-k">=</span> <span class="pl-v">self</span>._normal_observation_with_units(q_n_obs_name, experiment.true_injection_heats, experiment.observed_injection_heats, tau, ureg.microcalorie)</td>
      </tr>
      <tr>
        <td id="L615" class="blob-num js-line-number" data-line-number="615"></td>
        <td id="LC615" class="blob-code js-file-line">            <span class="pl-v">self</span>.stochastics.append(experiment.observation)</td>
      </tr>
      <tr>
        <td id="L616" class="blob-num js-line-number" data-line-number="616"></td>
        <td id="LC616" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L617" class="blob-num js-line-number" data-line-number="617"></td>
        <td id="LC617" class="blob-code js-file-line">        <span class="pl-c"># Create sampler.</span></td>
      </tr>
      <tr>
        <td id="L618" class="blob-num js-line-number" data-line-number="618"></td>
        <td id="LC618" class="blob-code js-file-line">        logger.info(<span class="pl-s"><span class="pl-pds">&quot;</span>Creating sampler...<span class="pl-pds">&quot;</span></span>)</td>
      </tr>
      <tr>
        <td id="L619" class="blob-num js-line-number" data-line-number="619"></td>
        <td id="LC619" class="blob-code js-file-line">        mcmc <span class="pl-k">=</span> <span class="pl-v">self</span>._create_metropolis_sampler()</td>
      </tr>
      <tr>
        <td id="L620" class="blob-num js-line-number" data-line-number="620"></td>
        <td id="LC620" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L621" class="blob-num js-line-number" data-line-number="621"></td>
        <td id="LC621" class="blob-code js-file-line">        <span class="pl-v">self</span>.mcmc <span class="pl-k">=</span> mcmc</td>
      </tr>
      <tr>
        <td id="L622" class="blob-num js-line-number" data-line-number="622"></td>
        <td id="LC622" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L623" class="blob-num js-line-number" data-line-number="623"></td>
        <td id="LC623" class="blob-code js-file-line">    <span class="pl-en">@<span class="pl-c1">staticmethod</span></span></td>
      </tr>
      <tr>
        <td id="L624" class="blob-num js-line-number" data-line-number="624"></td>
        <td id="LC624" class="blob-code js-file-line">    <span class="pl-k">def</span> <span class="pl-en">equilibrium_concentrations</span>(<span class="pl-smi">Ka_n</span>, <span class="pl-smi">C0_R</span>, <span class="pl-smi">C0_Ln</span>, <span class="pl-smi">V</span>, <span class="pl-smi">c0</span><span class="pl-k">=</span><span class="pl-c1">None</span>):</td>
      </tr>
      <tr>
        <td id="L625" class="blob-num js-line-number" data-line-number="625"></td>
        <td id="LC625" class="blob-code js-file-line">        <span class="pl-s"><span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L626" class="blob-num js-line-number" data-line-number="626"></td>
        <td id="LC626" class="blob-code js-file-line"><span class="pl-s">        Compute the equilibrium concentrations of each complex species for N ligands competitively binding to a receptor.</span></td>
      </tr>
      <tr>
        <td id="L627" class="blob-num js-line-number" data-line-number="627"></td>
        <td id="LC627" class="blob-code js-file-line"><span class="pl-s">        ARGUMENTS</span></td>
      </tr>
      <tr>
        <td id="L628" class="blob-num js-line-number" data-line-number="628"></td>
        <td id="LC628" class="blob-code js-file-line"><span class="pl-s">        Ka_n (numpy N-array of float) - Ka_n[n] is the association constant for receptor and ligand species n (1/M)</span></td>
      </tr>
      <tr>
        <td id="L629" class="blob-num js-line-number" data-line-number="629"></td>
        <td id="LC629" class="blob-code js-file-line"><span class="pl-s">        x_R (float) - the total number of moles of receptor in the sample volume</span></td>
      </tr>
      <tr>
        <td id="L630" class="blob-num js-line-number" data-line-number="630"></td>
        <td id="LC630" class="blob-code js-file-line"><span class="pl-s">        x_n (numpy N-array of float) - x_n[n] is the total number of moles of ligand species n in the sample volume</span></td>
      </tr>
      <tr>
        <td id="L631" class="blob-num js-line-number" data-line-number="631"></td>
        <td id="LC631" class="blob-code js-file-line"><span class="pl-s">        V (float) - the total sample volume (L)</span></td>
      </tr>
      <tr>
        <td id="L632" class="blob-num js-line-number" data-line-number="632"></td>
        <td id="LC632" class="blob-code js-file-line"><span class="pl-s">        RETURNS</span></td>
      </tr>
      <tr>
        <td id="L633" class="blob-num js-line-number" data-line-number="633"></td>
        <td id="LC633" class="blob-code js-file-line"><span class="pl-s">        C_n (numpy N-array of float) - C_n[n] is the concentration of complex of receptor with ligand species n</span></td>
      </tr>
      <tr>
        <td id="L634" class="blob-num js-line-number" data-line-number="634"></td>
        <td id="LC634" class="blob-code js-file-line"><span class="pl-s">        EXAMPLES</span></td>
      </tr>
      <tr>
        <td id="L635" class="blob-num js-line-number" data-line-number="635"></td>
        <td id="LC635" class="blob-code js-file-line"><span class="pl-s">        &gt;&gt;&gt; V = 1.4303e-3 # volume (L)</span></td>
      </tr>
      <tr>
        <td id="L636" class="blob-num js-line-number" data-line-number="636"></td>
        <td id="LC636" class="blob-code js-file-line"><span class="pl-s">        &gt;&gt;&gt; x_R = V * 510.e-3 # receptor</span></td>
      </tr>
      <tr>
        <td id="L637" class="blob-num js-line-number" data-line-number="637"></td>
        <td id="LC637" class="blob-code js-file-line"><span class="pl-s">        &gt;&gt;&gt; x_Ln = numpy.array([V * 8.6e-6, 200.e-6 * 55.e-6]) # ligands</span></td>
      </tr>
      <tr>
        <td id="L638" class="blob-num js-line-number" data-line-number="638"></td>
        <td id="LC638" class="blob-code js-file-line"><span class="pl-s">        &gt;&gt;&gt; Ka_n = numpy.array([1./(400.e-9), 1./(2.e-11)]) # association constants</span></td>
      </tr>
      <tr>
        <td id="L639" class="blob-num js-line-number" data-line-number="639"></td>
        <td id="LC639" class="blob-code js-file-line"><span class="pl-s">        &gt;&gt;&gt; C_PLn = equilibrium_concentrations(Ka_n, x_R, x_Ln, V)</span></td>
      </tr>
      <tr>
        <td id="L640" class="blob-num js-line-number" data-line-number="640"></td>
        <td id="LC640" class="blob-code js-file-line"><span class="pl-s">        NOTES</span></td>
      </tr>
      <tr>
        <td id="L641" class="blob-num js-line-number" data-line-number="641"></td>
        <td id="LC641" class="blob-code js-file-line"><span class="pl-s">        Each complex concentration C_n must obey the relation</span></td>
      </tr>
      <tr>
        <td id="L642" class="blob-num js-line-number" data-line-number="642"></td>
        <td id="LC642" class="blob-code js-file-line"><span class="pl-s">        Ka_n[n] = C_RLn[n] / (C_R * C_Ln[n])           for n = 1..N</span></td>
      </tr>
      <tr>
        <td id="L643" class="blob-num js-line-number" data-line-number="643"></td>
        <td id="LC643" class="blob-code js-file-line"><span class="pl-s">        with conservation of mass constraints</span></td>
      </tr>
      <tr>
        <td id="L644" class="blob-num js-line-number" data-line-number="644"></td>
        <td id="LC644" class="blob-code js-file-line"><span class="pl-s">        V * (C_Ln[n] + C_RLn[n]) = x_Ln[n]             for n = 1..N</span></td>
      </tr>
      <tr>
        <td id="L645" class="blob-num js-line-number" data-line-number="645"></td>
        <td id="LC645" class="blob-code js-file-line"><span class="pl-s">        and</span></td>
      </tr>
      <tr>
        <td id="L646" class="blob-num js-line-number" data-line-number="646"></td>
        <td id="LC646" class="blob-code js-file-line"><span class="pl-s">        V * (C_R + C_RLn[:].sum()) = x_R</span></td>
      </tr>
      <tr>
        <td id="L647" class="blob-num js-line-number" data-line-number="647"></td>
        <td id="LC647" class="blob-code js-file-line"><span class="pl-s">        along with the constraints</span></td>
      </tr>
      <tr>
        <td id="L648" class="blob-num js-line-number" data-line-number="648"></td>
        <td id="LC648" class="blob-code js-file-line"><span class="pl-s">        0 &lt;= V * C_RLn[n] &lt;= min(x_Ln[n], x_R)         for n = 1..N</span></td>
      </tr>
      <tr>
        <td id="L649" class="blob-num js-line-number" data-line-number="649"></td>
        <td id="LC649" class="blob-code js-file-line"><span class="pl-s">        V * C_RLn[:].sum() &lt;= x_R</span></td>
      </tr>
      <tr>
        <td id="L650" class="blob-num js-line-number" data-line-number="650"></td>
        <td id="LC650" class="blob-code js-file-line"><span class="pl-s">        We can rearrange these expressions to give</span></td>
      </tr>
      <tr>
        <td id="L651" class="blob-num js-line-number" data-line-number="651"></td>
        <td id="LC651" class="blob-code js-file-line"><span class="pl-s">        V * C_R * C_Ln[n] * Ka_n[n] - V * C_RLn[n] = 0</span></td>
      </tr>
      <tr>
        <td id="L652" class="blob-num js-line-number" data-line-number="652"></td>
        <td id="LC652" class="blob-code js-file-line"><span class="pl-s">        and eliminate C_Ln[n] and C_R to give</span></td>
      </tr>
      <tr>
        <td id="L653" class="blob-num js-line-number" data-line-number="653"></td>
        <td id="LC653" class="blob-code js-file-line"><span class="pl-s">        V * (x_R/V - C_RLn[:].sum()) * (x_Ln[n]/V - C_RLn[n]) * Ka_n[n] - V * C_RLn[n] = 0    for n = 1..N</span></td>
      </tr>
      <tr>
        <td id="L654" class="blob-num js-line-number" data-line-number="654"></td>
        <td id="LC654" class="blob-code js-file-line"><span class="pl-s">        <span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L655" class="blob-num js-line-number" data-line-number="655"></td>
        <td id="LC655" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L656" class="blob-num js-line-number" data-line-number="656"></td>
        <td id="LC656" class="blob-code js-file-line">        x_R <span class="pl-k">=</span> C0_R <span class="pl-k">*</span> V</td>
      </tr>
      <tr>
        <td id="L657" class="blob-num js-line-number" data-line-number="657"></td>
        <td id="LC657" class="blob-code js-file-line">        x_Ln <span class="pl-k">=</span> C0_Ln <span class="pl-k">*</span> V</td>
      </tr>
      <tr>
        <td id="L658" class="blob-num js-line-number" data-line-number="658"></td>
        <td id="LC658" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L659" class="blob-num js-line-number" data-line-number="659"></td>
        <td id="LC659" class="blob-code js-file-line">        nspecies <span class="pl-k">=</span> Ka_n.size</td>
      </tr>
      <tr>
        <td id="L660" class="blob-num js-line-number" data-line-number="660"></td>
        <td id="LC660" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L661" class="blob-num js-line-number" data-line-number="661"></td>
        <td id="LC661" class="blob-code js-file-line">        <span class="pl-c"># Define optimization functions</span></td>
      </tr>
      <tr>
        <td id="L662" class="blob-num js-line-number" data-line-number="662"></td>
        <td id="LC662" class="blob-code js-file-line">        <span class="pl-k">def</span> <span class="pl-en">func</span>(<span class="pl-smi">C_RLn</span>):</td>
      </tr>
      <tr>
        <td id="L663" class="blob-num js-line-number" data-line-number="663"></td>
        <td id="LC663" class="blob-code js-file-line">            f_n <span class="pl-k">=</span> V <span class="pl-k">*</span> (x_R <span class="pl-k">/</span> V <span class="pl-k">-</span> C_RLn[:].sum()) <span class="pl-k">*</span> (x_Ln[:] <span class="pl-k">/</span> V <span class="pl-k">-</span> C_RLn[:]) <span class="pl-k">*</span> Ka_n[:] <span class="pl-k">-</span> V <span class="pl-k">*</span> C_RLn[:]</td>
      </tr>
      <tr>
        <td id="L664" class="blob-num js-line-number" data-line-number="664"></td>
        <td id="LC664" class="blob-code js-file-line">            <span class="pl-k">return</span> f_n</td>
      </tr>
      <tr>
        <td id="L665" class="blob-num js-line-number" data-line-number="665"></td>
        <td id="LC665" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L666" class="blob-num js-line-number" data-line-number="666"></td>
        <td id="LC666" class="blob-code js-file-line">        <span class="pl-k">def</span> <span class="pl-en">fprime</span>(<span class="pl-smi">C_RLn</span>):</td>
      </tr>
      <tr>
        <td id="L667" class="blob-num js-line-number" data-line-number="667"></td>
        <td id="LC667" class="blob-code js-file-line">            nspecies <span class="pl-k">=</span> C_RLn.size</td>
      </tr>
      <tr>
        <td id="L668" class="blob-num js-line-number" data-line-number="668"></td>
        <td id="LC668" class="blob-code js-file-line">            <span class="pl-c"># G_nm[n,m] is the derivative of func[n] with respect to C_RLn[m]</span></td>
      </tr>
      <tr>
        <td id="L669" class="blob-num js-line-number" data-line-number="669"></td>
        <td id="LC669" class="blob-code js-file-line">            G_nm <span class="pl-k">=</span> numpy.zeros([nspecies, nspecies], numpy.float64)</td>
      </tr>
      <tr>
        <td id="L670" class="blob-num js-line-number" data-line-number="670"></td>
        <td id="LC670" class="blob-code js-file-line">            <span class="pl-k">for</span> n <span class="pl-k">in</span> <span class="pl-c1">range</span>(nspecies):</td>
      </tr>
      <tr>
        <td id="L671" class="blob-num js-line-number" data-line-number="671"></td>
        <td id="LC671" class="blob-code js-file-line">                G_nm[n, :] <span class="pl-k">=</span> <span class="pl-k">-</span> V <span class="pl-k">*</span> (x_Ln[:] <span class="pl-k">/</span> V <span class="pl-k">-</span> C_RLn[:]) <span class="pl-k">*</span> Ka_n[:]</td>
      </tr>
      <tr>
        <td id="L672" class="blob-num js-line-number" data-line-number="672"></td>
        <td id="LC672" class="blob-code js-file-line">                G_nm[n, n] <span class="pl-k">-=</span> V <span class="pl-k">*</span> (Ka_n[n] <span class="pl-k">*</span> (x_R <span class="pl-k">/</span> V <span class="pl-k">-</span> C_RLn[:].sum()) <span class="pl-k">+</span> <span class="pl-c1">1.0</span>)</td>
      </tr>
      <tr>
        <td id="L673" class="blob-num js-line-number" data-line-number="673"></td>
        <td id="LC673" class="blob-code js-file-line">            <span class="pl-k">return</span> G_nm</td>
      </tr>
      <tr>
        <td id="L674" class="blob-num js-line-number" data-line-number="674"></td>
        <td id="LC674" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L675" class="blob-num js-line-number" data-line-number="675"></td>
        <td id="LC675" class="blob-code js-file-line">        <span class="pl-k">def</span> <span class="pl-en">sfunc</span>(<span class="pl-smi">s</span>):</td>
      </tr>
      <tr>
        <td id="L676" class="blob-num js-line-number" data-line-number="676"></td>
        <td id="LC676" class="blob-code js-file-line">            f_n <span class="pl-k">=</span> V <span class="pl-k">*</span> (x_R <span class="pl-k">/</span> V <span class="pl-k">-</span> (s[:] <span class="pl-k">**</span> <span class="pl-c1">2</span>).sum()) <span class="pl-k">*</span> (x_Ln[:] <span class="pl-k">/</span> V <span class="pl-k">-</span> s[:] <span class="pl-k">**</span> <span class="pl-c1">2</span>) <span class="pl-k">*</span> Ka_n[:] <span class="pl-k">-</span> V <span class="pl-k">*</span> s[:] <span class="pl-k">**</span> <span class="pl-c1">2</span></td>
      </tr>
      <tr>
        <td id="L677" class="blob-num js-line-number" data-line-number="677"></td>
        <td id="LC677" class="blob-code js-file-line">            <span class="pl-k">return</span> f_n</td>
      </tr>
      <tr>
        <td id="L678" class="blob-num js-line-number" data-line-number="678"></td>
        <td id="LC678" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L679" class="blob-num js-line-number" data-line-number="679"></td>
        <td id="LC679" class="blob-code js-file-line">        <span class="pl-k">def</span> <span class="pl-en">sfprime</span>(<span class="pl-smi">s</span>):</td>
      </tr>
      <tr>
        <td id="L680" class="blob-num js-line-number" data-line-number="680"></td>
        <td id="LC680" class="blob-code js-file-line">            nspecies <span class="pl-k">=</span> s.size</td>
      </tr>
      <tr>
        <td id="L681" class="blob-num js-line-number" data-line-number="681"></td>
        <td id="LC681" class="blob-code js-file-line">            <span class="pl-c"># G_nm[n,m] is the derivative of func[n] with respect to C_RLn[m]</span></td>
      </tr>
      <tr>
        <td id="L682" class="blob-num js-line-number" data-line-number="682"></td>
        <td id="LC682" class="blob-code js-file-line">            G_nm <span class="pl-k">=</span> numpy.zeros([nspecies, nspecies], numpy.float64)</td>
      </tr>
      <tr>
        <td id="L683" class="blob-num js-line-number" data-line-number="683"></td>
        <td id="LC683" class="blob-code js-file-line">            <span class="pl-k">for</span> n <span class="pl-k">in</span> <span class="pl-c1">range</span>(nspecies):</td>
      </tr>
      <tr>
        <td id="L684" class="blob-num js-line-number" data-line-number="684"></td>
        <td id="LC684" class="blob-code js-file-line">                G_nm[n, :] <span class="pl-k">=</span> <span class="pl-k">-</span> V <span class="pl-k">*</span> (x_Ln[:] <span class="pl-k">/</span> V <span class="pl-k">-</span> s[:] <span class="pl-k">**</span> <span class="pl-c1">2</span>) <span class="pl-k">*</span> Ka_n[:]</td>
      </tr>
      <tr>
        <td id="L685" class="blob-num js-line-number" data-line-number="685"></td>
        <td id="LC685" class="blob-code js-file-line">                G_nm[n, n] <span class="pl-k">-=</span> V <span class="pl-k">*</span> (Ka_n[n] <span class="pl-k">*</span> (x_R <span class="pl-k">/</span> V <span class="pl-k">-</span> (s[:] <span class="pl-k">**</span> <span class="pl-c1">2</span>).sum()) <span class="pl-k">+</span> <span class="pl-c1">1.0</span>)</td>
      </tr>
      <tr>
        <td id="L686" class="blob-num js-line-number" data-line-number="686"></td>
        <td id="LC686" class="blob-code js-file-line">                G_nm[n, :] <span class="pl-k">*=</span> <span class="pl-c1">2.</span> <span class="pl-k">*</span> s[n]</td>
      </tr>
      <tr>
        <td id="L687" class="blob-num js-line-number" data-line-number="687"></td>
        <td id="LC687" class="blob-code js-file-line">            <span class="pl-k">return</span> G_nm</td>
      </tr>
      <tr>
        <td id="L688" class="blob-num js-line-number" data-line-number="688"></td>
        <td id="LC688" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L689" class="blob-num js-line-number" data-line-number="689"></td>
        <td id="LC689" class="blob-code js-file-line">        <span class="pl-k">def</span> <span class="pl-en">objective</span>(<span class="pl-smi">x</span>):</td>
      </tr>
      <tr>
        <td id="L690" class="blob-num js-line-number" data-line-number="690"></td>
        <td id="LC690" class="blob-code js-file-line">            f_n <span class="pl-k">=</span> func(x)</td>
      </tr>
      <tr>
        <td id="L691" class="blob-num js-line-number" data-line-number="691"></td>
        <td id="LC691" class="blob-code js-file-line">            G_nm <span class="pl-k">=</span> fprime(x)</td>
      </tr>
      <tr>
        <td id="L692" class="blob-num js-line-number" data-line-number="692"></td>
        <td id="LC692" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L693" class="blob-num js-line-number" data-line-number="693"></td>
        <td id="LC693" class="blob-code js-file-line">            obj <span class="pl-k">=</span> (f_n <span class="pl-k">**</span> <span class="pl-c1">2</span>).sum()</td>
      </tr>
      <tr>
        <td id="L694" class="blob-num js-line-number" data-line-number="694"></td>
        <td id="LC694" class="blob-code js-file-line">            grad <span class="pl-k">=</span> <span class="pl-c1">0.0</span> <span class="pl-k">*</span> f_n</td>
      </tr>
      <tr>
        <td id="L695" class="blob-num js-line-number" data-line-number="695"></td>
        <td id="LC695" class="blob-code js-file-line">            <span class="pl-k">for</span> n <span class="pl-k">in</span> <span class="pl-c1">range</span>(f_n.size):</td>
      </tr>
      <tr>
        <td id="L696" class="blob-num js-line-number" data-line-number="696"></td>
        <td id="LC696" class="blob-code js-file-line">                grad <span class="pl-k">+=</span> <span class="pl-c1">2</span> <span class="pl-k">*</span> f_n[n] <span class="pl-k">*</span> G_nm[n, :]</td>
      </tr>
      <tr>
        <td id="L697" class="blob-num js-line-number" data-line-number="697"></td>
        <td id="LC697" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L698" class="blob-num js-line-number" data-line-number="698"></td>
        <td id="LC698" class="blob-code js-file-line">            <span class="pl-k">return</span> (obj, grad)</td>
      </tr>
      <tr>
        <td id="L699" class="blob-num js-line-number" data-line-number="699"></td>
        <td id="LC699" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L700" class="blob-num js-line-number" data-line-number="700"></td>
        <td id="LC700" class="blob-code js-file-line">        <span class="pl-k">def</span> <span class="pl-en">ode</span>(<span class="pl-smi">c_n</span>, <span class="pl-smi">t</span>, <span class="pl-smi">Ka_n</span>, <span class="pl-smi">x_Ln</span>, <span class="pl-smi">x_R</span>):</td>
      </tr>
      <tr>
        <td id="L701" class="blob-num js-line-number" data-line-number="701"></td>
        <td id="LC701" class="blob-code js-file-line">            dc_n <span class="pl-k">=</span> <span class="pl-k">-</span> c_n[:] <span class="pl-k">+</span> Ka_n[:] <span class="pl-k">*</span> (x_Ln[:] <span class="pl-k">/</span> V <span class="pl-k">-</span> c_n[:]) <span class="pl-k">*</span> (x_R <span class="pl-k">/</span> V <span class="pl-k">-</span> c_n[:].sum())</td>
      </tr>
      <tr>
        <td id="L702" class="blob-num js-line-number" data-line-number="702"></td>
        <td id="LC702" class="blob-code js-file-line">            <span class="pl-k">return</span> dc_n</td>
      </tr>
      <tr>
        <td id="L703" class="blob-num js-line-number" data-line-number="703"></td>
        <td id="LC703" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L704" class="blob-num js-line-number" data-line-number="704"></td>
        <td id="LC704" class="blob-code js-file-line">        <span class="pl-k">def</span> <span class="pl-en">odegrad</span>(<span class="pl-smi">c_n</span>, <span class="pl-smi">t</span>, <span class="pl-smi">Ka_n</span>, <span class="pl-smi">x_Ln</span>, <span class="pl-smi">x_R</span>):</td>
      </tr>
      <tr>
        <td id="L705" class="blob-num js-line-number" data-line-number="705"></td>
        <td id="LC705" class="blob-code js-file-line">            N <span class="pl-k">=</span> c_n.size</td>
      </tr>
      <tr>
        <td id="L706" class="blob-num js-line-number" data-line-number="706"></td>
        <td id="LC706" class="blob-code js-file-line">            d2c <span class="pl-k">=</span> numpy.zeros([N, N], numpy.float64)</td>
      </tr>
      <tr>
        <td id="L707" class="blob-num js-line-number" data-line-number="707"></td>
        <td id="LC707" class="blob-code js-file-line">            <span class="pl-k">for</span> n <span class="pl-k">in</span> <span class="pl-c1">range</span>(N):</td>
      </tr>
      <tr>
        <td id="L708" class="blob-num js-line-number" data-line-number="708"></td>
        <td id="LC708" class="blob-code js-file-line">                d2c[n, :] <span class="pl-k">=</span> <span class="pl-k">-</span>Ka_n[n] <span class="pl-k">*</span> (x_Ln[n] <span class="pl-k">/</span> V <span class="pl-k">-</span> c_n[n])</td>
      </tr>
      <tr>
        <td id="L709" class="blob-num js-line-number" data-line-number="709"></td>
        <td id="LC709" class="blob-code js-file-line">                d2c[n, n] <span class="pl-k">+=</span> <span class="pl-k">-</span>(Ka_n[n] <span class="pl-k">*</span> (x_R <span class="pl-k">/</span> V <span class="pl-k">-</span> c_n[:].sum()) <span class="pl-k">+</span> <span class="pl-c1">1.0</span>)</td>
      </tr>
      <tr>
        <td id="L710" class="blob-num js-line-number" data-line-number="710"></td>
        <td id="LC710" class="blob-code js-file-line">            <span class="pl-k">return</span> d2c</td>
      </tr>
      <tr>
        <td id="L711" class="blob-num js-line-number" data-line-number="711"></td>
        <td id="LC711" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L712" class="blob-num js-line-number" data-line-number="712"></td>
        <td id="LC712" class="blob-code js-file-line">        c <span class="pl-k">=</span> numpy.zeros([nspecies], numpy.float64)</td>
      </tr>
      <tr>
        <td id="L713" class="blob-num js-line-number" data-line-number="713"></td>
        <td id="LC713" class="blob-code js-file-line">        sorted_indices <span class="pl-k">=</span> numpy.argsort(<span class="pl-k">-</span>x_Ln)</td>
      </tr>
      <tr>
        <td id="L714" class="blob-num js-line-number" data-line-number="714"></td>
        <td id="LC714" class="blob-code js-file-line">        <span class="pl-k">for</span> n <span class="pl-k">in</span> <span class="pl-c1">range</span>(nspecies):</td>
      </tr>
      <tr>
        <td id="L715" class="blob-num js-line-number" data-line-number="715"></td>
        <td id="LC715" class="blob-code js-file-line">            indices <span class="pl-k">=</span> sorted_indices[<span class="pl-c1">0</span>:n <span class="pl-k">+</span> <span class="pl-c1">1</span>]</td>
      </tr>
      <tr>
        <td id="L716" class="blob-num js-line-number" data-line-number="716"></td>
        <td id="LC716" class="blob-code js-file-line">            c[indices] <span class="pl-k">=</span> scipy.optimize.fsolve(ode, c[indices], <span class="pl-smi">fprime</span><span class="pl-k">=</span>odegrad, <span class="pl-smi">args</span><span class="pl-k">=</span>(<span class="pl-c1">0.0</span>, Ka_n[indices], x_Ln[indices], x_R), <span class="pl-smi">xtol</span><span class="pl-k">=</span><span class="pl-c1">1.0e-6</span>)</td>
      </tr>
      <tr>
        <td id="L717" class="blob-num js-line-number" data-line-number="717"></td>
        <td id="LC717" class="blob-code js-file-line">        C_RLn <span class="pl-k">=</span> c</td>
      </tr>
      <tr>
        <td id="L718" class="blob-num js-line-number" data-line-number="718"></td>
        <td id="LC718" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L719" class="blob-num js-line-number" data-line-number="719"></td>
        <td id="LC719" class="blob-code js-file-line">        <span class="pl-k">return</span> C_RLn</td>
      </tr>
      <tr>
        <td id="L720" class="blob-num js-line-number" data-line-number="720"></td>
        <td id="LC720" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L721" class="blob-num js-line-number" data-line-number="721"></td>
        <td id="LC721" class="blob-code js-file-line">    <span class="pl-en">@<span class="pl-c1">staticmethod</span></span></td>
      </tr>
      <tr>
        <td id="L722" class="blob-num js-line-number" data-line-number="722"></td>
        <td id="LC722" class="blob-code js-file-line">    <span class="pl-en">@</span><span class="pl-en">ureg.wraps</span>(<span class="pl-smi">ret</span><span class="pl-k">=</span>ureg.calorie, <span class="pl-smi">args</span><span class="pl-k">=</span>[<span class="pl-c1">None</span>, <span class="pl-c1">None</span>, ureg.liter, <span class="pl-c1">None</span>, ureg.liter, ureg.mole <span class="pl-k">/</span> ureg.kilocalorie, <span class="pl-c1">None</span>, <span class="pl-c1">None</span>, <span class="pl-c1">None</span>, <span class="pl-c1">None</span>])</td>
      </tr>
      <tr>
        <td id="L723" class="blob-num js-line-number" data-line-number="723"></td>
        <td id="LC723" class="blob-code js-file-line">    <span class="pl-k">def</span> <span class="pl-en">expected_injection_heats</span>(<span class="pl-smi">ligands</span>, <span class="pl-smi">receptor</span>, <span class="pl-smi">V0</span>, <span class="pl-smi">N</span>, <span class="pl-smi">volumes</span>, <span class="pl-smi">beta</span>, <span class="pl-smi">true_cell_concentration</span>, <span class="pl-smi">true_syringe_concentration</span>, <span class="pl-smi">DeltaH_0</span>, <span class="pl-smi">thermodynamic_parameters</span>):</td>
      </tr>
      <tr>
        <td id="L724" class="blob-num js-line-number" data-line-number="724"></td>
        <td id="LC724" class="blob-code js-file-line">        <span class="pl-s"><span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L725" class="blob-num js-line-number" data-line-number="725"></td>
        <td id="LC725" class="blob-code js-file-line"><span class="pl-s">        Expected heats of injection for two-component binding model.</span></td>
      </tr>
      <tr>
        <td id="L726" class="blob-num js-line-number" data-line-number="726"></td>
        <td id="LC726" class="blob-code js-file-line"><span class="pl-s">        ligands - set of strings containing ligand name</span></td>
      </tr>
      <tr>
        <td id="L727" class="blob-num js-line-number" data-line-number="727"></td>
        <td id="LC727" class="blob-code js-file-line"><span class="pl-s">        receptor - string with receptor name</span></td>
      </tr>
      <tr>
        <td id="L728" class="blob-num js-line-number" data-line-number="728"></td>
        <td id="LC728" class="blob-code js-file-line"><span class="pl-s">        V0 - cell volume in liters</span></td>
      </tr>
      <tr>
        <td id="L729" class="blob-num js-line-number" data-line-number="729"></td>
        <td id="LC729" class="blob-code js-file-line"><span class="pl-s">        N - int number of injections</span></td>
      </tr>
      <tr>
        <td id="L730" class="blob-num js-line-number" data-line-number="730"></td>
        <td id="LC730" class="blob-code js-file-line"><span class="pl-s">        volumes - injection volumes in liters</span></td>
      </tr>
      <tr>
        <td id="L731" class="blob-num js-line-number" data-line-number="731"></td>
        <td id="LC731" class="blob-code js-file-line"><span class="pl-s">        beta = 1 over temperature * R, in mole / kcal</span></td>
      </tr>
      <tr>
        <td id="L732" class="blob-num js-line-number" data-line-number="732"></td>
        <td id="LC732" class="blob-code js-file-line"><span class="pl-s">        true_cell_concentration - (dict of floats) - concentrations[species] is the initial concentration of species in sample cell, or zero if absent (mM)</span></td>
      </tr>
      <tr>
        <td id="L733" class="blob-num js-line-number" data-line-number="733"></td>
        <td id="LC733" class="blob-code js-file-line"><span class="pl-s">        true_syringe_concentration (dict of floats) - concentrations[species] is the initial concentration of species in sample cell, or zero if absent (mM)</span></td>
      </tr>
      <tr>
        <td id="L734" class="blob-num js-line-number" data-line-number="734"></td>
        <td id="LC734" class="blob-code js-file-line"><span class="pl-s">        DeltaH_0, heat of injection (cal)</span></td>
      </tr>
      <tr>
        <td id="L735" class="blob-num js-line-number" data-line-number="735"></td>
        <td id="LC735" class="blob-code js-file-line"><span class="pl-s">        thermodynamic_parameters (dict of floats) - thermodynamic_parameters[parameter] is the value of thermodynamic parameter (kcal/mol)</span></td>
      </tr>
      <tr>
        <td id="L736" class="blob-num js-line-number" data-line-number="736"></td>
        <td id="LC736" class="blob-code js-file-line"><span class="pl-s">          e.g. for parameter &#39;DeltaG of receptor * species&#39;</span></td>
      </tr>
      <tr>
        <td id="L737" class="blob-num js-line-number" data-line-number="737"></td>
        <td id="LC737" class="blob-code js-file-line"><span class="pl-s">        <span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L738" class="blob-num js-line-number" data-line-number="738"></td>
        <td id="LC738" class="blob-code js-file-line">        <span class="pl-c"># Number of ligand species</span></td>
      </tr>
      <tr>
        <td id="L739" class="blob-num js-line-number" data-line-number="739"></td>
        <td id="LC739" class="blob-code js-file-line">        nspecies <span class="pl-k">=</span> <span class="pl-c1">len</span>(ligands)</td>
      </tr>
      <tr>
        <td id="L740" class="blob-num js-line-number" data-line-number="740"></td>
        <td id="LC740" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L741" class="blob-num js-line-number" data-line-number="741"></td>
        <td id="LC741" class="blob-code js-file-line">        <span class="pl-c"># Compute association constants for receptor and each ligand species.</span></td>
      </tr>
      <tr>
        <td id="L742" class="blob-num js-line-number" data-line-number="742"></td>
        <td id="LC742" class="blob-code js-file-line">        DeltaG_n <span class="pl-k">=</span> numpy.zeros([nspecies], numpy.float64)</td>
      </tr>
      <tr>
        <td id="L743" class="blob-num js-line-number" data-line-number="743"></td>
        <td id="LC743" class="blob-code js-file-line">        <span class="pl-k">for</span> (n, ligand) <span class="pl-k">in</span> <span class="pl-c1">enumerate</span>(ligands):</td>
      </tr>
      <tr>
        <td id="L744" class="blob-num js-line-number" data-line-number="744"></td>
        <td id="LC744" class="blob-code js-file-line">            <span class="pl-c"># determine name of free energy of binding for this ligand</span></td>
      </tr>
      <tr>
        <td id="L745" class="blob-num js-line-number" data-line-number="745"></td>
        <td id="LC745" class="blob-code js-file-line">            name <span class="pl-k">=</span> <span class="pl-s"><span class="pl-pds">&quot;</span>DeltaG of <span class="pl-c1">%s</span> * <span class="pl-c1">%s</span><span class="pl-pds">&quot;</span></span> <span class="pl-k">%</span> (receptor, ligand)</td>
      </tr>
      <tr>
        <td id="L746" class="blob-num js-line-number" data-line-number="746"></td>
        <td id="LC746" class="blob-code js-file-line">            <span class="pl-c"># retrieve free energy of binding</span></td>
      </tr>
      <tr>
        <td id="L747" class="blob-num js-line-number" data-line-number="747"></td>
        <td id="LC747" class="blob-code js-file-line">            DeltaG_n[n] <span class="pl-k">=</span> thermodynamic_parameters[name]</td>
      </tr>
      <tr>
        <td id="L748" class="blob-num js-line-number" data-line-number="748"></td>
        <td id="LC748" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L749" class="blob-num js-line-number" data-line-number="749"></td>
        <td id="LC749" class="blob-code js-file-line">        <span class="pl-c"># compute association constant (1/M)</span></td>
      </tr>
      <tr>
        <td id="L750" class="blob-num js-line-number" data-line-number="750"></td>
        <td id="LC750" class="blob-code js-file-line">        Ka_n <span class="pl-k">=</span> numpy.exp(<span class="pl-k">-</span>beta <span class="pl-k">*</span> DeltaG_n[:])</td>
      </tr>
      <tr>
        <td id="L751" class="blob-num js-line-number" data-line-number="751"></td>
        <td id="LC751" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L752" class="blob-num js-line-number" data-line-number="752"></td>
        <td id="LC752" class="blob-code js-file-line">        <span class="pl-c"># Compute the quantity of each species in the sample cell after each injection.</span></td>
      </tr>
      <tr>
        <td id="L753" class="blob-num js-line-number" data-line-number="753"></td>
        <td id="LC753" class="blob-code js-file-line">        <span class="pl-c"># NOTE: These quantities are correct for a perfusion-type model.  This would be modified for a cumulative model.</span></td>
      </tr>
      <tr>
        <td id="L754" class="blob-num js-line-number" data-line-number="754"></td>
        <td id="LC754" class="blob-code js-file-line">        <span class="pl-c"># x_Ri[i] is the number of moles of receptor in sample cell after injection i</span></td>
      </tr>
      <tr>
        <td id="L755" class="blob-num js-line-number" data-line-number="755"></td>
        <td id="LC755" class="blob-code js-file-line">        x_Ri <span class="pl-k">=</span> numpy.zeros([N], numpy.float64)</td>
      </tr>
      <tr>
        <td id="L756" class="blob-num js-line-number" data-line-number="756"></td>
        <td id="LC756" class="blob-code js-file-line">        <span class="pl-c"># x_Lin[i,n] is the number of moles of ligand n in sample cell after injection i</span></td>
      </tr>
      <tr>
        <td id="L757" class="blob-num js-line-number" data-line-number="757"></td>
        <td id="LC757" class="blob-code js-file-line">        x_Lin <span class="pl-k">=</span> numpy.zeros([N, nspecies], numpy.float64)</td>
      </tr>
      <tr>
        <td id="L758" class="blob-num js-line-number" data-line-number="758"></td>
        <td id="LC758" class="blob-code js-file-line">        dcum <span class="pl-k">=</span> <span class="pl-c1">1.0</span>  <span class="pl-c"># cumulative dilution factor</span></td>
      </tr>
      <tr>
        <td id="L759" class="blob-num js-line-number" data-line-number="759"></td>
        <td id="LC759" class="blob-code js-file-line">        <span class="pl-k">for</span> index, volume <span class="pl-k">in</span> <span class="pl-c1">enumerate</span>(volumes):</td>
      </tr>
      <tr>
        <td id="L760" class="blob-num js-line-number" data-line-number="760"></td>
        <td id="LC760" class="blob-code js-file-line">            d <span class="pl-k">=</span> <span class="pl-c1">1.0</span> <span class="pl-k">-</span> (volume <span class="pl-k">/</span> V0)  <span class="pl-c"># dilution factor (dimensionless)</span></td>
      </tr>
      <tr>
        <td id="L761" class="blob-num js-line-number" data-line-number="761"></td>
        <td id="LC761" class="blob-code js-file-line">            dcum <span class="pl-k">*=</span> d  <span class="pl-c"># cumulative dilution factor (dimensionless)</span></td>
      </tr>
      <tr>
        <td id="L762" class="blob-num js-line-number" data-line-number="762"></td>
        <td id="LC762" class="blob-code js-file-line">            x_Ri[index] <span class="pl-k">=</span> true_cell_concentration[receptor] <span class="pl-k">*</span> <span class="pl-c1">1.e-3</span> <span class="pl-k">*</span> dcum <span class="pl-k">+</span> true_syringe_concentration[receptor] <span class="pl-k">*</span> <span class="pl-c1">1.e-3</span> <span class="pl-k">*</span> (<span class="pl-c1">1.0</span> <span class="pl-k">-</span> dcum)</td>
      </tr>
      <tr>
        <td id="L763" class="blob-num js-line-number" data-line-number="763"></td>
        <td id="LC763" class="blob-code js-file-line">            <span class="pl-k">for</span> (n, ligand) <span class="pl-k">in</span> <span class="pl-c1">enumerate</span>(ligands):</td>
      </tr>
      <tr>
        <td id="L764" class="blob-num js-line-number" data-line-number="764"></td>
        <td id="LC764" class="blob-code js-file-line">                x_Lin[index, n] <span class="pl-k">=</span> true_cell_concentration[ligand] <span class="pl-k">*</span> <span class="pl-c1">1.e-3</span> <span class="pl-k">*</span> dcum <span class="pl-k">+</span> true_syringe_concentration[ligand] <span class="pl-k">*</span> <span class="pl-c1">1.e-3</span> <span class="pl-k">*</span> (<span class="pl-c1">1.0</span> <span class="pl-k">-</span> dcum)</td>
      </tr>
      <tr>
        <td id="L765" class="blob-num js-line-number" data-line-number="765"></td>
        <td id="LC765" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L766" class="blob-num js-line-number" data-line-number="766"></td>
        <td id="LC766" class="blob-code js-file-line">        <span class="pl-c"># Solve for initial concentration.</span></td>
      </tr>
      <tr>
        <td id="L767" class="blob-num js-line-number" data-line-number="767"></td>
        <td id="LC767" class="blob-code js-file-line">        x_R0 <span class="pl-k">=</span> true_cell_concentration[receptor] <span class="pl-k">*</span> <span class="pl-c1">1.e-3</span></td>
      </tr>
      <tr>
        <td id="L768" class="blob-num js-line-number" data-line-number="768"></td>
        <td id="LC768" class="blob-code js-file-line">        x_L0n <span class="pl-k">=</span> numpy.zeros([nspecies], numpy.float64)</td>
      </tr>
      <tr>
        <td id="L769" class="blob-num js-line-number" data-line-number="769"></td>
        <td id="LC769" class="blob-code js-file-line">        C_RL0n <span class="pl-k">=</span> numpy.zeros([nspecies], numpy.float64)</td>
      </tr>
      <tr>
        <td id="L770" class="blob-num js-line-number" data-line-number="770"></td>
        <td id="LC770" class="blob-code js-file-line">        <span class="pl-k">for</span> (n, ligand) <span class="pl-k">in</span> <span class="pl-c1">enumerate</span>(ligands):</td>
      </tr>
      <tr>
        <td id="L771" class="blob-num js-line-number" data-line-number="771"></td>
        <td id="LC771" class="blob-code js-file-line">            x_L0n[n] <span class="pl-k">=</span> true_cell_concentration[ligand] <span class="pl-k">*</span> <span class="pl-c1">1.e-3</span></td>
      </tr>
      <tr>
        <td id="L772" class="blob-num js-line-number" data-line-number="772"></td>
        <td id="LC772" class="blob-code js-file-line">        C_RL0n[:] <span class="pl-k">=</span> CompetitiveBindingModel.equilibrium_concentrations(Ka_n, x_R0, x_L0n[:], V0)</td>
      </tr>
      <tr>
        <td id="L773" class="blob-num js-line-number" data-line-number="773"></td>
        <td id="LC773" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L774" class="blob-num js-line-number" data-line-number="774"></td>
        <td id="LC774" class="blob-code js-file-line">        <span class="pl-c"># Compute complex concentrations after each injection.</span></td>
      </tr>
      <tr>
        <td id="L775" class="blob-num js-line-number" data-line-number="775"></td>
        <td id="LC775" class="blob-code js-file-line">        <span class="pl-c"># NOTE: The total cell volume would be modified for a cumulative model.</span></td>
      </tr>
      <tr>
        <td id="L776" class="blob-num js-line-number" data-line-number="776"></td>
        <td id="LC776" class="blob-code js-file-line">        <span class="pl-c"># C_RLin[i,n] is the concentration of complex RLn[n] after injection i</span></td>
      </tr>
      <tr>
        <td id="L777" class="blob-num js-line-number" data-line-number="777"></td>
        <td id="LC777" class="blob-code js-file-line">        C_RLin <span class="pl-k">=</span> numpy.zeros([N, nspecies], numpy.float64)</td>
      </tr>
      <tr>
        <td id="L778" class="blob-num js-line-number" data-line-number="778"></td>
        <td id="LC778" class="blob-code js-file-line">        <span class="pl-k">for</span> index <span class="pl-k">in</span> <span class="pl-c1">range</span>(N):</td>
      </tr>
      <tr>
        <td id="L779" class="blob-num js-line-number" data-line-number="779"></td>
        <td id="LC779" class="blob-code js-file-line">            C_RLin[index, :] <span class="pl-k">=</span> CompetitiveBindingModel.equilibrium_concentrations(Ka_n, x_Ri[index], x_Lin[index, :], V0)</td>
      </tr>
      <tr>
        <td id="L780" class="blob-num js-line-number" data-line-number="780"></td>
        <td id="LC780" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L781" class="blob-num js-line-number" data-line-number="781"></td>
        <td id="LC781" class="blob-code js-file-line">        <span class="pl-c"># Compile a list of thermodynamic parameters.</span></td>
      </tr>
      <tr>
        <td id="L782" class="blob-num js-line-number" data-line-number="782"></td>
        <td id="LC782" class="blob-code js-file-line">        <span class="pl-c"># DeltaH_n[n] is the enthalpy of association of ligand species n</span></td>
      </tr>
      <tr>
        <td id="L783" class="blob-num js-line-number" data-line-number="783"></td>
        <td id="LC783" class="blob-code js-file-line">        DeltaH_n <span class="pl-k">=</span> numpy.zeros([nspecies], numpy.float64)</td>
      </tr>
      <tr>
        <td id="L784" class="blob-num js-line-number" data-line-number="784"></td>
        <td id="LC784" class="blob-code js-file-line">        <span class="pl-k">for</span> (n, ligand) <span class="pl-k">in</span> <span class="pl-c1">enumerate</span>(ligands):</td>
      </tr>
      <tr>
        <td id="L785" class="blob-num js-line-number" data-line-number="785"></td>
        <td id="LC785" class="blob-code js-file-line">            name <span class="pl-k">=</span> <span class="pl-s"><span class="pl-pds">&quot;</span>DeltaH of <span class="pl-c1">%s</span> * <span class="pl-c1">%s</span><span class="pl-pds">&quot;</span></span> <span class="pl-k">%</span> (receptor, ligand)</td>
      </tr>
      <tr>
        <td id="L786" class="blob-num js-line-number" data-line-number="786"></td>
        <td id="LC786" class="blob-code js-file-line">            DeltaH_n[n] <span class="pl-k">=</span> thermodynamic_parameters[name]</td>
      </tr>
      <tr>
        <td id="L787" class="blob-num js-line-number" data-line-number="787"></td>
        <td id="LC787" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L788" class="blob-num js-line-number" data-line-number="788"></td>
        <td id="LC788" class="blob-code js-file-line">        <span class="pl-c"># Compute expected injection heats.</span></td>
      </tr>
      <tr>
        <td id="L789" class="blob-num js-line-number" data-line-number="789"></td>
        <td id="LC789" class="blob-code js-file-line">        <span class="pl-c"># NOTE: This is for an instantaneous injection / perfusion model.</span></td>
      </tr>
      <tr>
        <td id="L790" class="blob-num js-line-number" data-line-number="790"></td>
        <td id="LC790" class="blob-code js-file-line">        q_n <span class="pl-k">=</span> DeltaH_0 <span class="pl-k">*</span> numpy.ones([N], numpy.float64)</td>
      </tr>
      <tr>
        <td id="L791" class="blob-num js-line-number" data-line-number="791"></td>
        <td id="LC791" class="blob-code js-file-line">        d <span class="pl-k">=</span> <span class="pl-c1">1.0</span> <span class="pl-k">-</span> (volumes[<span class="pl-c1">0</span>] <span class="pl-k">/</span> V0)  <span class="pl-c"># dilution factor (dimensionless)</span></td>
      </tr>
      <tr>
        <td id="L792" class="blob-num js-line-number" data-line-number="792"></td>
        <td id="LC792" class="blob-code js-file-line">        <span class="pl-k">for</span> n <span class="pl-k">in</span> <span class="pl-c1">range</span>(nspecies):</td>
      </tr>
      <tr>
        <td id="L793" class="blob-num js-line-number" data-line-number="793"></td>
        <td id="LC793" class="blob-code js-file-line">            q_n[<span class="pl-c1">0</span>] <span class="pl-k">+=</span> (<span class="pl-c1">1000.0</span> <span class="pl-k">*</span> DeltaH_n[n]) <span class="pl-k">*</span> V0 <span class="pl-k">*</span> (C_RLin[<span class="pl-c1">0</span>, n] <span class="pl-k">-</span> d <span class="pl-k">*</span> C_RL0n[n])  <span class="pl-c"># first injection</span></td>
      </tr>
      <tr>
        <td id="L794" class="blob-num js-line-number" data-line-number="794"></td>
        <td id="LC794" class="blob-code js-file-line">        <span class="pl-k">for</span> index, volume <span class="pl-k">in</span> <span class="pl-c1">enumerate</span>(volumes[<span class="pl-c1">1</span>:], <span class="pl-smi">start</span><span class="pl-k">=</span><span class="pl-c1">1</span>):</td>
      </tr>
      <tr>
        <td id="L795" class="blob-num js-line-number" data-line-number="795"></td>
        <td id="LC795" class="blob-code js-file-line">            d <span class="pl-k">=</span> <span class="pl-c1">1.0</span> <span class="pl-k">-</span> (volume <span class="pl-k">/</span> V0)  <span class="pl-c"># dilution factor (dimensionless)</span></td>
      </tr>
      <tr>
        <td id="L796" class="blob-num js-line-number" data-line-number="796"></td>
        <td id="LC796" class="blob-code js-file-line">            <span class="pl-k">for</span> n <span class="pl-k">in</span> <span class="pl-c1">range</span>(nspecies):</td>
      </tr>
      <tr>
        <td id="L797" class="blob-num js-line-number" data-line-number="797"></td>
        <td id="LC797" class="blob-code js-file-line">                <span class="pl-c"># subsequent injections</span></td>
      </tr>
      <tr>
        <td id="L798" class="blob-num js-line-number" data-line-number="798"></td>
        <td id="LC798" class="blob-code js-file-line">                q_n[index] <span class="pl-k">+=</span> (<span class="pl-c1">1000.0</span> <span class="pl-k">*</span> DeltaH_n[n]) <span class="pl-k">*</span> V0 <span class="pl-k">*</span> (C_RLin[index, n] <span class="pl-k">-</span> d <span class="pl-k">*</span> C_RLin[index <span class="pl-k">-</span> <span class="pl-c1">1</span>, n])</td>
      </tr>
      <tr>
        <td id="L799" class="blob-num js-line-number" data-line-number="799"></td>
        <td id="LC799" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L800" class="blob-num js-line-number" data-line-number="800"></td>
        <td id="LC800" class="blob-code js-file-line">        <span class="pl-k">return</span> q_n</td>
      </tr>
      <tr>
        <td id="L801" class="blob-num js-line-number" data-line-number="801"></td>
        <td id="LC801" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L802" class="blob-num js-line-number" data-line-number="802"></td>
        <td id="LC802" class="blob-code js-file-line">    <span class="pl-k">def</span> <span class="pl-en">_create_rescaling_sampler</span>(<span class="pl-smi">self</span>, <span class="pl-smi">receptor</span>):</td>
      </tr>
      <tr>
        <td id="L803" class="blob-num js-line-number" data-line-number="803"></td>
        <td id="LC803" class="blob-code js-file-line">        <span class="pl-s"><span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L804" class="blob-num js-line-number" data-line-number="804"></td>
        <td id="LC804" class="blob-code js-file-line"><span class="pl-s">        Create a sampler that uses RescalingStep for correlated variables</span></td>
      </tr>
      <tr>
        <td id="L805" class="blob-num js-line-number" data-line-number="805"></td>
        <td id="LC805" class="blob-code js-file-line"><span class="pl-s">        <span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L806" class="blob-num js-line-number" data-line-number="806"></td>
        <td id="LC806" class="blob-code js-file-line">        mcmc <span class="pl-k">=</span> <span class="pl-v">self</span>._create_metropolis_sampler()</td>
      </tr>
      <tr>
        <td id="L807" class="blob-num js-line-number" data-line-number="807"></td>
        <td id="LC807" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L808" class="blob-num js-line-number" data-line-number="808"></td>
        <td id="LC808" class="blob-code js-file-line">        <span class="pl-k">for</span> experiment <span class="pl-k">in</span> <span class="pl-v">self</span>.experiments:</td>
      </tr>
      <tr>
        <td id="L809" class="blob-num js-line-number" data-line-number="809"></td>
        <td id="LC809" class="blob-code js-file-line">            <span class="pl-k">for</span> ligand <span class="pl-k">in</span> <span class="pl-v">self</span>.ligands:</td>
      </tr>
      <tr>
        <td id="L810" class="blob-num js-line-number" data-line-number="810"></td>
        <td id="LC810" class="blob-code js-file-line">                <span class="pl-k">if</span> <span class="pl-c1">isinstance</span>(experiment.true_syringe_concentration[ligand], pymc.distributions.Lognormal):</td>
      </tr>
      <tr>
        <td id="L811" class="blob-num js-line-number" data-line-number="811"></td>
        <td id="LC811" class="blob-code js-file-line">                    mcmc.use_step_method(RescalingStep, {<span class="pl-s"><span class="pl-pds">&#39;</span>Ls<span class="pl-pds">&#39;</span></span>: experiment.true_syringe_concentration[ligand],</td>
      </tr>
      <tr>
        <td id="L812" class="blob-num js-line-number" data-line-number="812"></td>
        <td id="LC812" class="blob-code js-file-line">                                                         <span class="pl-s"><span class="pl-pds">&#39;</span>P0<span class="pl-pds">&#39;</span></span>: experiment.true_cell_concentration[receptor],</td>
      </tr>
      <tr>
        <td id="L813" class="blob-num js-line-number" data-line-number="813"></td>
        <td id="LC813" class="blob-code js-file-line">                                                         <span class="pl-s"><span class="pl-pds">&#39;</span>DeltaH<span class="pl-pds">&#39;</span></span>: <span class="pl-v">self</span>.thermodynamic_parameters[</td>
      </tr>
      <tr>
        <td id="L814" class="blob-num js-line-number" data-line-number="814"></td>
        <td id="LC814" class="blob-code js-file-line">                                                             <span class="pl-s"><span class="pl-pds">&#39;</span>DeltaH of <span class="pl-c1">%s</span> * <span class="pl-c1">%s</span><span class="pl-pds">&#39;</span></span> <span class="pl-k">%</span> (receptor, ligand)],</td>
      </tr>
      <tr>
        <td id="L815" class="blob-num js-line-number" data-line-number="815"></td>
        <td id="LC815" class="blob-code js-file-line">                                                         <span class="pl-s"><span class="pl-pds">&#39;</span>DeltaG<span class="pl-pds">&#39;</span></span>: <span class="pl-v">self</span>.thermodynamic_parameters[</td>
      </tr>
      <tr>
        <td id="L816" class="blob-num js-line-number" data-line-number="816"></td>
        <td id="LC816" class="blob-code js-file-line">                                                             <span class="pl-s"><span class="pl-pds">&#39;</span>DeltaG of <span class="pl-c1">%s</span> * <span class="pl-c1">%s</span><span class="pl-pds">&#39;</span></span> <span class="pl-k">%</span> (receptor, ligand)]}, <span class="pl-v">self</span>.beta)</td>
      </tr>
      <tr>
        <td id="L817" class="blob-num js-line-number" data-line-number="817"></td>
        <td id="LC817" class="blob-code js-file-line">        <span class="pl-k">return</span> mcmc</td>
      </tr>
      <tr>
        <td id="L818" class="blob-num js-line-number" data-line-number="818"></td>
        <td id="LC818" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L819" class="blob-num js-line-number" data-line-number="819"></td>
        <td id="LC819" class="blob-code js-file-line">    <span class="pl-k">def</span> <span class="pl-en">_create_metropolis_sampler</span>(<span class="pl-smi">self</span>):</td>
      </tr>
      <tr>
        <td id="L820" class="blob-num js-line-number" data-line-number="820"></td>
        <td id="LC820" class="blob-code js-file-line">        <span class="pl-s"><span class="pl-pds">&quot;&quot;&quot;</span>Create a simple metropolis sampler for each stochastic<span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L821" class="blob-num js-line-number" data-line-number="821"></td>
        <td id="LC821" class="blob-code js-file-line">        mcmc <span class="pl-k">=</span> pymc.MCMC(<span class="pl-v">self</span>.stochastics, <span class="pl-smi">db</span><span class="pl-k">=</span><span class="pl-s"><span class="pl-pds">&#39;</span>ram<span class="pl-pds">&#39;</span></span>)</td>
      </tr>
      <tr>
        <td id="L822" class="blob-num js-line-number" data-line-number="822"></td>
        <td id="LC822" class="blob-code js-file-line">        <span class="pl-k">for</span> stochastic <span class="pl-k">in</span> <span class="pl-v">self</span>.stochastics:</td>
      </tr>
      <tr>
        <td id="L823" class="blob-num js-line-number" data-line-number="823"></td>
        <td id="LC823" class="blob-code js-file-line">            <span class="pl-c"># print stochastic</span></td>
      </tr>
      <tr>
        <td id="L824" class="blob-num js-line-number" data-line-number="824"></td>
        <td id="LC824" class="blob-code js-file-line">            <span class="pl-k">try</span>:</td>
      </tr>
      <tr>
        <td id="L825" class="blob-num js-line-number" data-line-number="825"></td>
        <td id="LC825" class="blob-code js-file-line">                mcmc.use_step_method(pymc.Metropolis, stochastic)</td>
      </tr>
      <tr>
        <td id="L826" class="blob-num js-line-number" data-line-number="826"></td>
        <td id="LC826" class="blob-code js-file-line">            <span class="pl-k">except</span> <span class="pl-c1">Exception</span>:</td>
      </tr>
      <tr>
        <td id="L827" class="blob-num js-line-number" data-line-number="827"></td>
        <td id="LC827" class="blob-code js-file-line">                <span class="pl-k">pass</span></td>
      </tr>
      <tr>
        <td id="L828" class="blob-num js-line-number" data-line-number="828"></td>
        <td id="LC828" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L829" class="blob-num js-line-number" data-line-number="829"></td>
        <td id="LC829" class="blob-code js-file-line">        <span class="pl-k">return</span> mcmc</td>
      </tr>
      <tr>
        <td id="L830" class="blob-num js-line-number" data-line-number="830"></td>
        <td id="LC830" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L831" class="blob-num js-line-number" data-line-number="831"></td>
        <td id="LC831" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L832" class="blob-num js-line-number" data-line-number="832"></td>
        <td id="LC832" class="blob-code js-file-line">    <span class="pl-k">def</span> <span class="pl-en">_lambda_heats_model</span>(<span class="pl-smi">self</span>, <span class="pl-smi">experiment</span>, <span class="pl-smi">q_name</span>):</td>
      </tr>
      <tr>
        <td id="L833" class="blob-num js-line-number" data-line-number="833"></td>
        <td id="LC833" class="blob-code js-file-line">        <span class="pl-s"><span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L834" class="blob-num js-line-number" data-line-number="834"></td>
        <td id="LC834" class="blob-code js-file-line"><span class="pl-s">        Model the heat using expected_injection_heats, providing all input by using a lambda function</span></td>
      </tr>
      <tr>
        <td id="L835" class="blob-num js-line-number" data-line-number="835"></td>
        <td id="LC835" class="blob-code js-file-line"><span class="pl-s">        q_name is the name for the model</span></td>
      </tr>
      <tr>
        <td id="L836" class="blob-num js-line-number" data-line-number="836"></td>
        <td id="LC836" class="blob-code js-file-line"><span class="pl-s">        <span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L837" class="blob-num js-line-number" data-line-number="837"></td>
        <td id="LC837" class="blob-code js-file-line">        <span class="pl-k">return</span> pymc.Lambda(q_name,</td>
      </tr>
      <tr>
        <td id="L838" class="blob-num js-line-number" data-line-number="838"></td>
        <td id="LC838" class="blob-code js-file-line">                           <span class="pl-k">lambda</span></td>
      </tr>
      <tr>
        <td id="L839" class="blob-num js-line-number" data-line-number="839"></td>
        <td id="LC839" class="blob-code js-file-line">                               <span class="pl-smi">ligands</span><span class="pl-k">=</span><span class="pl-v">self</span>.ligands,</td>
      </tr>
      <tr>
        <td id="L840" class="blob-num js-line-number" data-line-number="840"></td>
        <td id="LC840" class="blob-code js-file-line">                               <span class="pl-smi">receptor</span><span class="pl-k">=</span><span class="pl-v">self</span>.receptor,</td>
      </tr>
      <tr>
        <td id="L841" class="blob-num js-line-number" data-line-number="841"></td>
        <td id="LC841" class="blob-code js-file-line">                               <span class="pl-smi">V0</span><span class="pl-k">=</span><span class="pl-v">self</span>.V0,</td>
      </tr>
      <tr>
        <td id="L842" class="blob-num js-line-number" data-line-number="842"></td>
        <td id="LC842" class="blob-code js-file-line">                               <span class="pl-smi">N</span><span class="pl-k">=</span>experiment.ninjections,</td>
      </tr>
      <tr>
        <td id="L843" class="blob-num js-line-number" data-line-number="843"></td>
        <td id="LC843" class="blob-code js-file-line">                               <span class="pl-smi">volumes</span><span class="pl-k">=</span>experiment.injection_volumes,</td>
      </tr>
      <tr>
        <td id="L844" class="blob-num js-line-number" data-line-number="844"></td>
        <td id="LC844" class="blob-code js-file-line">                               <span class="pl-smi">beta</span><span class="pl-k">=</span><span class="pl-v">self</span>.beta,</td>
      </tr>
      <tr>
        <td id="L845" class="blob-num js-line-number" data-line-number="845"></td>
        <td id="LC845" class="blob-code js-file-line">                               <span class="pl-smi">cell_concentration</span><span class="pl-k">=</span>experiment.true_cell_concentration,</td>
      </tr>
      <tr>
        <td id="L846" class="blob-num js-line-number" data-line-number="846"></td>
        <td id="LC846" class="blob-code js-file-line">                               <span class="pl-smi">syringe_concentration</span><span class="pl-k">=</span>experiment.true_syringe_concentration,</td>
      </tr>
      <tr>
        <td id="L847" class="blob-num js-line-number" data-line-number="847"></td>
        <td id="LC847" class="blob-code js-file-line">                               <span class="pl-smi">DeltaH_0</span><span class="pl-k">=</span>experiment.DeltaH_0,</td>
      </tr>
      <tr>
        <td id="L848" class="blob-num js-line-number" data-line-number="848"></td>
        <td id="LC848" class="blob-code js-file-line">                               <span class="pl-smi">thermodynamic_parameters</span><span class="pl-k">=</span><span class="pl-v">self</span>.thermodynamic_parameters:</td>
      </tr>
      <tr>
        <td id="L849" class="blob-num js-line-number" data-line-number="849"></td>
        <td id="LC849" class="blob-code js-file-line">                           <span class="pl-v">self</span>.expected_injection_heats(</td>
      </tr>
      <tr>
        <td id="L850" class="blob-num js-line-number" data-line-number="850"></td>
        <td id="LC850" class="blob-code js-file-line">                               ligands,</td>
      </tr>
      <tr>
        <td id="L851" class="blob-num js-line-number" data-line-number="851"></td>
        <td id="LC851" class="blob-code js-file-line">                               receptor,</td>
      </tr>
      <tr>
        <td id="L852" class="blob-num js-line-number" data-line-number="852"></td>
        <td id="LC852" class="blob-code js-file-line">                               V0,</td>
      </tr>
      <tr>
        <td id="L853" class="blob-num js-line-number" data-line-number="853"></td>
        <td id="LC853" class="blob-code js-file-line">                               N,</td>
      </tr>
      <tr>
        <td id="L854" class="blob-num js-line-number" data-line-number="854"></td>
        <td id="LC854" class="blob-code js-file-line">                               volumes,</td>
      </tr>
      <tr>
        <td id="L855" class="blob-num js-line-number" data-line-number="855"></td>
        <td id="LC855" class="blob-code js-file-line">                               beta,</td>
      </tr>
      <tr>
        <td id="L856" class="blob-num js-line-number" data-line-number="856"></td>
        <td id="LC856" class="blob-code js-file-line">                               cell_concentration,</td>
      </tr>
      <tr>
        <td id="L857" class="blob-num js-line-number" data-line-number="857"></td>
        <td id="LC857" class="blob-code js-file-line">                               syringe_concentration,</td>
      </tr>
      <tr>
        <td id="L858" class="blob-num js-line-number" data-line-number="858"></td>
        <td id="LC858" class="blob-code js-file-line">                               DeltaH_0,</td>
      </tr>
      <tr>
        <td id="L859" class="blob-num js-line-number" data-line-number="859"></td>
        <td id="LC859" class="blob-code js-file-line">                               thermodynamic_parameters</td>
      </tr>
      <tr>
        <td id="L860" class="blob-num js-line-number" data-line-number="860"></td>
        <td id="LC860" class="blob-code js-file-line">                           )</td>
      </tr>
      <tr>
        <td id="L861" class="blob-num js-line-number" data-line-number="861"></td>
        <td id="LC861" class="blob-code js-file-line">        )</td>
      </tr>
      <tr>
        <td id="L862" class="blob-num js-line-number" data-line-number="862"></td>
        <td id="LC862" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L863" class="blob-num js-line-number" data-line-number="863"></td>
        <td id="LC863" class="blob-code js-file-line">    <span class="pl-k">def</span> <span class="pl-en">_logsigma_guesses_from_multiple_experiments</span>(<span class="pl-smi">self</span>, <span class="pl-smi">standard_unit</span>):</td>
      </tr>
      <tr>
        <td id="L864" class="blob-num js-line-number" data-line-number="864"></td>
        <td id="LC864" class="blob-code js-file-line">        <span class="pl-s"><span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L865" class="blob-num js-line-number" data-line-number="865"></td>
        <td id="LC865" class="blob-code js-file-line"><span class="pl-s">        standard_unit: unit by which to correct the magnitude of sigma</span></td>
      </tr>
      <tr>
        <td id="L866" class="blob-num js-line-number" data-line-number="866"></td>
        <td id="LC866" class="blob-code js-file-line"><span class="pl-s">        <span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L867" class="blob-num js-line-number" data-line-number="867"></td>
        <td id="LC867" class="blob-code js-file-line">        <span class="pl-c"># Determine min and max range for log_sigma (log of instrument heat measurement error)</span></td>
      </tr>
      <tr>
        <td id="L868" class="blob-num js-line-number" data-line-number="868"></td>
        <td id="LC868" class="blob-code js-file-line">        <span class="pl-c"># TODO: This should depend on a number of factors, like integration time, heat signal, etc.?</span></td>
      </tr>
      <tr>
        <td id="L869" class="blob-num js-line-number" data-line-number="869"></td>
        <td id="LC869" class="blob-code js-file-line">        sigma_guess <span class="pl-k">=</span> <span class="pl-c1">0.0</span></td>
      </tr>
      <tr>
        <td id="L870" class="blob-num js-line-number" data-line-number="870"></td>
        <td id="LC870" class="blob-code js-file-line">        <span class="pl-k">for</span> experiment <span class="pl-k">in</span> <span class="pl-v">self</span>.experiments:</td>
      </tr>
      <tr>
        <td id="L871" class="blob-num js-line-number" data-line-number="871"></td>
        <td id="LC871" class="blob-code js-file-line">            sigma_guess <span class="pl-k">+=</span> experiment.observed_injection_heats[:<span class="pl-k">-</span><span class="pl-c1">4</span>].std()</td>
      </tr>
      <tr>
        <td id="L872" class="blob-num js-line-number" data-line-number="872"></td>
        <td id="LC872" class="blob-code js-file-line">        sigma_guess <span class="pl-k">/=</span> <span class="pl-c1">float</span>(<span class="pl-c1">len</span>(<span class="pl-v">self</span>.experiments))</td>
      </tr>
      <tr>
        <td id="L873" class="blob-num js-line-number" data-line-number="873"></td>
        <td id="LC873" class="blob-code js-file-line">        log_sigma_guess <span class="pl-k">=</span> log(sigma_guess <span class="pl-k">/</span> standard_unit)</td>
      </tr>
      <tr>
        <td id="L874" class="blob-num js-line-number" data-line-number="874"></td>
        <td id="LC874" class="blob-code js-file-line">        log_sigma_min <span class="pl-k">=</span> log_sigma_guess <span class="pl-k">-</span> <span class="pl-c1">10</span></td>
      </tr>
      <tr>
        <td id="L875" class="blob-num js-line-number" data-line-number="875"></td>
        <td id="LC875" class="blob-code js-file-line">        log_sigma_max <span class="pl-k">=</span> log_sigma_guess <span class="pl-k">+</span> <span class="pl-c1">5</span></td>
      </tr>
      <tr>
        <td id="L876" class="blob-num js-line-number" data-line-number="876"></td>
        <td id="LC876" class="blob-code js-file-line">        <span class="pl-k">return</span> log_sigma_guess, log_sigma_max, log_sigma_min</td>
      </tr>
      <tr>
        <td id="L877" class="blob-num js-line-number" data-line-number="877"></td>
        <td id="LC877" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L878" class="blob-num js-line-number" data-line-number="878"></td>
        <td id="LC878" class="blob-code js-file-line">    <span class="pl-en">@<span class="pl-c1">staticmethod</span></span></td>
      </tr>
      <tr>
        <td id="L879" class="blob-num js-line-number" data-line-number="879"></td>
        <td id="LC879" class="blob-code js-file-line">    <span class="pl-k">def</span> <span class="pl-en">_species_from_experiments</span>(<span class="pl-smi">experiments</span>):</td>
      </tr>
      <tr>
        <td id="L880" class="blob-num js-line-number" data-line-number="880"></td>
        <td id="LC880" class="blob-code js-file-line">        species <span class="pl-k">=</span> <span class="pl-c1">set</span>()  <span class="pl-c"># all molecular species</span></td>
      </tr>
      <tr>
        <td id="L881" class="blob-num js-line-number" data-line-number="881"></td>
        <td id="LC881" class="blob-code js-file-line">        <span class="pl-k">for</span> experiment <span class="pl-k">in</span> experiments:</td>
      </tr>
      <tr>
        <td id="L882" class="blob-num js-line-number" data-line-number="882"></td>
        <td id="LC882" class="blob-code js-file-line">            species.update(experiment.cell_concentration.keys())</td>
      </tr>
      <tr>
        <td id="L883" class="blob-num js-line-number" data-line-number="883"></td>
        <td id="LC883" class="blob-code js-file-line">            species.update(experiment.syringe_concentration.keys())</td>
      </tr>
      <tr>
        <td id="L884" class="blob-num js-line-number" data-line-number="884"></td>
        <td id="LC884" class="blob-code js-file-line">        <span class="pl-k">return</span> species</td>
      </tr>
      <tr>
        <td id="L885" class="blob-num js-line-number" data-line-number="885"></td>
        <td id="LC885" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L886" class="blob-num js-line-number" data-line-number="886"></td>
        <td id="LC886" class="blob-code js-file-line">    <span class="pl-k">def</span> <span class="pl-en">_zero_for_missing__concentrations</span>(<span class="pl-smi">self</span>, <span class="pl-smi">experiment</span>):</td>
      </tr>
      <tr>
        <td id="L887" class="blob-num js-line-number" data-line-number="887"></td>
        <td id="LC887" class="blob-code js-file-line">        <span class="pl-k">for</span> species <span class="pl-k">in</span> <span class="pl-v">self</span>.species:</td>
      </tr>
      <tr>
        <td id="L888" class="blob-num js-line-number" data-line-number="888"></td>
        <td id="LC888" class="blob-code js-file-line">            <span class="pl-k">if</span> species <span class="pl-k">not</span> <span class="pl-k">in</span> experiment.true_cell_concentration:</td>
      </tr>
      <tr>
        <td id="L889" class="blob-num js-line-number" data-line-number="889"></td>
        <td id="LC889" class="blob-code js-file-line">                experiment.true_cell_concentration[species] <span class="pl-k">=</span> <span class="pl-c1">0.0</span></td>
      </tr>
      <tr>
        <td id="L890" class="blob-num js-line-number" data-line-number="890"></td>
        <td id="LC890" class="blob-code js-file-line">            <span class="pl-k">if</span> species <span class="pl-k">not</span> <span class="pl-k">in</span> experiment.true_syringe_concentration:</td>
      </tr>
      <tr>
        <td id="L891" class="blob-num js-line-number" data-line-number="891"></td>
        <td id="LC891" class="blob-code js-file-line">                experiment.true_syringe_concentration[species] <span class="pl-k">=</span> <span class="pl-c1">0.0</span></td>
      </tr>
      <tr>
        <td id="L892" class="blob-num js-line-number" data-line-number="892"></td>
        <td id="LC892" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L893" class="blob-num js-line-number" data-line-number="893"></td>
        <td id="LC893" class="blob-code js-file-line"><span class="pl-k">class</span> <span class="pl-en">RacemicMixtureBindingModel</span>(<span class="pl-e">CompetitiveBindingModel</span>):</td>
      </tr>
      <tr>
        <td id="L894" class="blob-num js-line-number" data-line-number="894"></td>
        <td id="LC894" class="blob-code js-file-line">    <span class="pl-s"><span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L895" class="blob-num js-line-number" data-line-number="895"></td>
        <td id="LC895" class="blob-code js-file-line"><span class="pl-s">    Racemic Mixture Binding Model</span></td>
      </tr>
      <tr>
        <td id="L896" class="blob-num js-line-number" data-line-number="896"></td>
        <td id="LC896" class="blob-code js-file-line"><span class="pl-s"></span></td>
      </tr>
      <tr>
        <td id="L897" class="blob-num js-line-number" data-line-number="897"></td>
        <td id="LC897" class="blob-code js-file-line"><span class="pl-s">    <span class="pl-pds">&quot;&quot;&quot;</span></span></td>
      </tr>
      <tr>
        <td id="L898" class="blob-num js-line-number" data-line-number="898"></td>
        <td id="LC898" class="blob-code js-file-line">    <span class="pl-k">def</span> <span class="pl-en">equilibrium_concentrations</span>(<span class="pl-smi">self</span>, <span class="pl-smi">Ka_n</span>, <span class="pl-smi">C0_R</span>, <span class="pl-smi">C0_Ln</span>, <span class="pl-smi">V</span>, <span class="pl-smi">c0</span><span class="pl-k">=</span><span class="pl-c1">None</span>):</td>
      </tr>
      <tr>
        <td id="L899" class="blob-num js-line-number" data-line-number="899"></td>
        <td id="LC899" class="blob-code js-file-line">      a <span class="pl-k">=</span> <span class="pl-c1">1.</span><span class="pl-k">/</span>Ka_n[<span class="pl-c1">0</span>] <span class="pl-k">+</span> <span class="pl-c1">1.</span><span class="pl-k">/</span>Ka_n[<span class="pl-c1">1</span>] <span class="pl-k">+</span> C0_Ln[<span class="pl-c1">0</span>] <span class="pl-k">+</span> C0_Ln[<span class="pl-c1">1</span>] <span class="pl-k">-</span> C0_R</td>
      </tr>
      <tr>
        <td id="L900" class="blob-num js-line-number" data-line-number="900"></td>
        <td id="LC900" class="blob-code js-file-line">      b <span class="pl-k">=</span> <span class="pl-c1">1.</span><span class="pl-k">/</span>Ka_n[<span class="pl-c1">1</span>]<span class="pl-k">*</span>(C0_Ln[<span class="pl-c1">0</span>]<span class="pl-k">-</span>C0_R) <span class="pl-k">+</span> <span class="pl-c1">1.</span><span class="pl-k">/</span>Ka_n[<span class="pl-c1">0</span>]<span class="pl-k">*</span>(C0_Ln[<span class="pl-c1">1</span>]<span class="pl-k">-</span>C0_R) <span class="pl-k">+</span> <span class="pl-c1">1.</span><span class="pl-k">/</span>Ka_n[<span class="pl-c1">0</span>]<span class="pl-k">*</span><span class="pl-c1">1.</span><span class="pl-k">/</span>Ka_n[<span class="pl-c1">1</span>]</td>
      </tr>
      <tr>
        <td id="L901" class="blob-num js-line-number" data-line-number="901"></td>
        <td id="LC901" class="blob-code js-file-line">      c <span class="pl-k">=</span> (<span class="pl-k">-</span><span class="pl-c1">1.</span><span class="pl-k">/</span>Ka_n[<span class="pl-c1">0</span>])<span class="pl-k">*</span><span class="pl-c1">1.</span><span class="pl-k">/</span>Ka_n[<span class="pl-c1">1</span>]<span class="pl-k">*</span>C0_R</td>
      </tr>
      <tr>
        <td id="L902" class="blob-num js-line-number" data-line-number="902"></td>
        <td id="LC902" class="blob-code js-file-line">      d <span class="pl-k">=</span> numpy.sqrt(a<span class="pl-k">*</span>a<span class="pl-k">-</span><span class="pl-c1">3</span><span class="pl-k">*</span>b)</td>
      </tr>
      <tr>
        <td id="L903" class="blob-num js-line-number" data-line-number="903"></td>
        <td id="LC903" class="blob-code js-file-line">      theta <span class="pl-k">=</span> numpy.arccos(((<span class="pl-k">-</span><span class="pl-c1">2.</span><span class="pl-k">*</span>a<span class="pl-k">**</span><span class="pl-c1">3</span>)<span class="pl-k">+</span><span class="pl-c1">9.</span><span class="pl-k">*</span>a<span class="pl-k">*</span>b<span class="pl-k">-</span><span class="pl-c1">27.</span><span class="pl-k">*</span>c)<span class="pl-k">/</span>(<span class="pl-c1">2.</span><span class="pl-k">*</span>(d<span class="pl-k">**</span><span class="pl-c1">3</span>)))</td>
      </tr>
      <tr>
        <td id="L904" class="blob-num js-line-number" data-line-number="904"></td>
        <td id="LC904" class="blob-code js-file-line">      PA <span class="pl-k">=</span> C0_Ln[<span class="pl-c1">0</span>]<span class="pl-k">*</span>(<span class="pl-c1">2.</span><span class="pl-k">*</span>d<span class="pl-k">*</span>numpy.cos(theta<span class="pl-k">/</span><span class="pl-c1">3.</span>)<span class="pl-k">-</span>a)<span class="pl-k">/</span>(<span class="pl-c1">3.</span><span class="pl-k">*</span><span class="pl-c1">1.</span><span class="pl-k">/</span>Ka_n[<span class="pl-c1">0</span>]<span class="pl-k">+</span>(<span class="pl-c1">2.</span><span class="pl-k">*</span>d<span class="pl-k">*</span>numpy.cos(theta<span class="pl-k">/</span><span class="pl-c1">3.</span>)<span class="pl-k">-</span>a))</td>
      </tr>
      <tr>
        <td id="L905" class="blob-num js-line-number" data-line-number="905"></td>
        <td id="LC905" class="blob-code js-file-line">      PB <span class="pl-k">=</span> C0_Ln[<span class="pl-c1">1</span>]<span class="pl-k">*</span>(<span class="pl-c1">2.</span><span class="pl-k">*</span>d<span class="pl-k">*</span>numpy.cos(theta<span class="pl-k">/</span><span class="pl-c1">3.</span>)<span class="pl-k">-</span>a)<span class="pl-k">/</span>(<span class="pl-c1">3.</span><span class="pl-k">*</span><span class="pl-c1">1.</span><span class="pl-k">/</span>Ka_n[<span class="pl-c1">1</span>]<span class="pl-k">+</span>(<span class="pl-c1">2.</span><span class="pl-k">*</span>d<span class="pl-k">*</span>numpy.cos(theta<span class="pl-k">/</span><span class="pl-c1">3.</span>)<span class="pl-k">-</span>a))</td>
      </tr>
      <tr>
        <td id="L906" class="blob-num js-line-number" data-line-number="906"></td>
        <td id="LC906" class="blob-code js-file-line">      <span class="pl-k">return</span> numpy.array([PA, PB])</td>
      </tr>
      <tr>
        <td id="L907" class="blob-num js-line-number" data-line-number="907"></td>
        <td id="LC907" class="blob-code js-file-line">
</td>
      </tr>
      <tr>
        <td id="L908" class="blob-num js-line-number" data-line-number="908"></td>
        <td id="LC908" class="blob-code js-file-line"><span class="pl-c"># Container of all models that this module provides for use</span></td>
      </tr>
      <tr>
        <td id="L909" class="blob-num js-line-number" data-line-number="909"></td>
        <td id="LC909" class="blob-code js-file-line">known_models <span class="pl-k">=</span> {<span class="pl-s"><span class="pl-pds">&#39;</span>TwoComponent<span class="pl-pds">&#39;</span></span>: TwoComponentBindingModel,</td>
      </tr>
      <tr>
        <td id="L910" class="blob-num js-line-number" data-line-number="910"></td>
        <td id="LC910" class="blob-code js-file-line">                <span class="pl-s"><span class="pl-pds">&#39;</span>Competitive<span class="pl-pds">&#39;</span></span>: CompetitiveBindingModel,</td>
      </tr>
      <tr>
        <td id="L911" class="blob-num js-line-number" data-line-number="911"></td>
        <td id="LC911" class="blob-code js-file-line">                <span class="pl-s"><span class="pl-pds">&#39;</span>RacemicMixture<span class="pl-pds">&#39;</span></span>: RacemicMixtureBindingModel</td>
      </tr>
      <tr>
        <td id="L912" class="blob-num js-line-number" data-line-number="912"></td>
        <td id="LC912" class="blob-code js-file-line">                }</td>
      </tr>
</table>

  </div>

</div>

<a href="#jump-to-line" rel="facebox[.linejump]" data-hotkey="l" style="display:none">Jump to Line</a>
<div id="jump-to-line" style="display:none">
  <form accept-charset="UTF-8" action="" class="js-jump-to-line-form" method="get"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /></div>
    <input class="linejump-input js-jump-to-line-field" type="text" placeholder="Jump to line&hellip;" autofocus>
    <button type="submit" class="btn">Go</button>
</form></div>

        </div>

      </div><!-- /.repo-container -->
      <div class="modal-backdrop"></div>
    </div><!-- /.container -->
  </div><!-- /.site -->


    </div><!-- /.wrapper -->

      <div class="container">
  <div class="site-footer" role="contentinfo">
    <ul class="site-footer-links right">
        <li><a href="https://status.github.com/" data-ga-click="Footer, go to status, text:status">Status</a></li>
      <li><a href="https://developer.github.com" data-ga-click="Footer, go to api, text:api">API</a></li>
      <li><a href="https://training.github.com" data-ga-click="Footer, go to training, text:training">Training</a></li>
      <li><a href="https://shop.github.com" data-ga-click="Footer, go to shop, text:shop">Shop</a></li>
        <li><a href="https://github.com/blog" data-ga-click="Footer, go to blog, text:blog">Blog</a></li>
        <li><a href="https://github.com/about" data-ga-click="Footer, go to about, text:about">About</a></li>

    </ul>

    <a href="https://github.com" aria-label="Homepage">
      <span class="mega-octicon octicon-mark-github" title="GitHub"></span>
</a>
    <ul class="site-footer-links">
      <li>&copy; 2015 <span title="0.15335s from github-fe127-cp1-prd.iad.github.net">GitHub</span>, Inc.</li>
        <li><a href="https://github.com/site/terms" data-ga-click="Footer, go to terms, text:terms">Terms</a></li>
        <li><a href="https://github.com/site/privacy" data-ga-click="Footer, go to privacy, text:privacy">Privacy</a></li>
        <li><a href="https://github.com/security" data-ga-click="Footer, go to security, text:security">Security</a></li>
        <li><a href="https://github.com/contact" data-ga-click="Footer, go to contact, text:contact">Contact</a></li>
    </ul>
  </div>
</div>


    <div class="fullscreen-overlay js-fullscreen-overlay" id="fullscreen_overlay">
  <div class="fullscreen-container js-suggester-container">
    <div class="textarea-wrap">
      <textarea name="fullscreen-contents" id="fullscreen-contents" class="fullscreen-contents js-fullscreen-contents" placeholder=""></textarea>
      <div class="suggester-container">
        <div class="suggester fullscreen-suggester js-suggester js-navigation-container"></div>
      </div>
    </div>
  </div>
  <div class="fullscreen-sidebar">
    <a href="#" class="exit-fullscreen js-exit-fullscreen tooltipped tooltipped-w" aria-label="Exit Zen Mode">
      <span class="mega-octicon octicon-screen-normal"></span>
    </a>
    <a href="#" class="theme-switcher js-theme-switcher tooltipped tooltipped-w"
      aria-label="Switch themes">
      <span class="octicon octicon-color-mode"></span>
    </a>
  </div>
</div>



    
    

    <div id="ajax-error-message" class="flash flash-error">
      <span class="octicon octicon-alert"></span>
      <a href="#" class="octicon octicon-x flash-close js-ajax-error-dismiss" aria-label="Dismiss error"></a>
      Something went wrong with that request. Please try again.
    </div>


      <script crossorigin="anonymous" src="https://assets-cdn.github.com/assets/frameworks-2c8ae50712a47d2b83d740cb875d55cdbbb3fdbccf303951cc6b7e63731e0c38.js"></script>
      <script async="async" crossorigin="anonymous" src="https://assets-cdn.github.com/assets/github-ccbcc7b50227d5a885caa9792908fae68ab0e93d60952d62068fe7b7357ac797.js"></script>
      
      


  </body>
</html>


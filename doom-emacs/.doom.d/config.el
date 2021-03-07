;;; $DOOMDIR/config.el -*- lexical-binding: t; -*-

;; Place your private configuration here! Remember, you do not need to run 'doom
;; sync' after modifying this file!


;; Some functionality uses this to identify you, e.g. GPG configuration, email
;; clients, file templates and snippets.
(setq user-full-name "David Budzynski"
      user-mail-address "john@doe.com")

;; Doom exposes five (optional) variables for controlling fonts in Doom. Here
;; are the three important ones:
;;
;; + `doom-font'
;; + `doom-variable-pitch-font'
;; + `doom-big-font' -- used for `doom-big-font-mode'; use this for
;;   presentations or streaming.
;;
;; They all accept either a font-spec, font string ("Input Mono-12"), or xlfd
;; font string. You generally only need these two:
(setq doom-font (font-spec :family "SFMono Nerd Font Mono" :size 15 :weight 'medium)
       doom-variable-pitch-font (font-spec :family "SFMono Nerd Font Mono" :size 16))

;; There are two ways to load a theme. Both assume the theme is installed and
;; available. You can either set `doom-theme' or manually load a theme with the
;; `load-theme' function. This is the default:
(setq doom-theme 'doom-gruvbox)

;; set opacity
;;(set-frame-parameter (selected-frame) 'alpha '(<active> . <inactive>))
;;(set-frame-parameter (selected-frame) 'alpha <both>)
(set-frame-parameter (selected-frame) 'alpha '(97 . 97))
(add-to-list 'default-frame-alist '(alpha . (97 . 97)))

;; If you use `org' and don't want your org files in the default location below,
;; change `org-directory'. It must be set before org loads!
(setq org-directory "~/org/")

;; This determines the style of line numbers in effect. If set to `nil', line
;; numbers are disabled. For relative line numbers, set this to `relative'.
(setq display-line-numbers-type `relative)


;; Here are some additional functions/macros that could help you configure Doom:
;;
;; - `load!' for loading external *.el files relative to this one
;; - `use-package!' for configuring packages
;; - `after!' for running code after a package has loaded
;; - `add-load-path!' for adding directories to the `load-path', relative to
;;   this file. Emacs searches the `load-path' when you load packages with
;;   `require' or `use-package'.
;; - `map!' for binding new keys
;;
;; To get information about any of these functions/macros, move the cursor over
;; the highlighted symbol at press 'K' (non-evil users must press 'C-c c k').
;; This will open documentation for it, including demos of how they are used.
;;
;; You can also try 'gd' (or 'C-c c d') to jump to their definition and see how
;; they are implemented.

(after! git-gutter-fringe
  (fringe-mode '14))

;; when using stow or any other dofile version control system, add this so that
;; doom knows to not throw lining erros in its emacs lisp files
(add-to-list '+emacs-lisp-disable-flycheck-in-dirs "~/dotfiles/doom-emacs/.doom.d/")

;; enable visual enhancements for elfeed
(elfeed-goodies/setup)

;; by default show articles from two weeks back
(after! elfeed
  (setq elfeed-search-filter "@2-weeks-ago +unread"))

;;Automatically updating feed when opening elfeed
(add-hook! 'elfeed-search-mode-hook 'elfeed-update)

(setq elfeed-feeds
        ;; hacker news
      '(("https://hnrss.org/frontpage" news)
        ;; unix sheikh
        ("https://unixsheikh.com/feed.rss" blog BSD)
        ;; mental outlaw YT
        ("https://www.youtube.com/feeds/videos.xml?channel_id=UC7YOGHUfC1Tb6E4pudI9STA" yt tech linux)
        ;; Irreal
        ("https://irreal.org/blog/?feed=rss2" blog emacs)
        ;; Broadie Robertson YT
        ("https://www.youtube.com/feeds/videos.xml?channel_id=UCld68syR8Wi-GY_n4CaoJGA" yt tech linux)
        ;; Luke Smith YT
        ("https://www.youtube.com/feeds/videos.xml?channel_id=UC2eYFnH61tmytImy1mTYvhA" yt tech linux)
        ;; DistroTube YT
        ("https://www.youtube.com/feeds/videos.xml?channel_id=UCVls1GmFKf6WlTraIb_IaJg" yt tech linux)
        ;; SyntaxFM podcast
        ("http://feed.syntax.fm/rss" podcast tech web-dev)
        ;; Lex Fridman podcast
        ("https://lexfridman.com/feed/podcast/" podcast tech)
        ;; System Crafters YT
        ("https://www.youtube.com/feeds/videos.xml?channel_id=UCAiiOTio8Yu69c3XnR7nQBQ" emacs tech yt)
        ;; Arch Linux Latest News
        ("https://archlinux.org/feeds/news/" linux news tech)
        ;; FreeBSD News
        ("https://www.freebsd.org/news/feed.xml" BSD news)
        ))

;; open any link with youtube in the url in mpv
;; this prevents from opening the link in a browser
;; so not ideal
;; (defun browse-url-mpv (url &optional new-window)
;;     (start-process "mpv" "*mpv*" "mpv" url))
;; (setq browse-url-browser-function '(("https:\\/\\/www\\.youtube." . browse-url-mpv)
;;                                     ("." . browse-url-firefox)))

;; download the video in elfeed using youtube-dl
(defun yt-dl-it (url)
  "Downloads the URL in an async shell"
  (let ((default-directory "~/Videos"))
    (async-shell-command (format "noglob youtube-dl %s" url))))

(defun elfeed-youtube-dl (&optional use-generic-p)
  "Youtube-DL link"
  (interactive "P")
  (let ((entries (elfeed-search-selected)))
    (cl-loop for entry in entries
             do (elfeed-untag entry 'unread)
             when (elfeed-entry-link entry)
             do (yt-dl-it it))
    (mapc #'elfeed-search-update-entry entries)
    (unless (use-region-p) (forward-line))))

(define-key elfeed-search-mode-map (kbd "d") 'elfeed-youtube-dl)

;; play the video in mpv
(defun elfeed-v-mpv (url)
  "Watch a video from URL in MPV"
   (start-process "mpv" "*mpv*" "mpv" url))
  ;; (async-shell-command (format "noglob mpv %s" url)))

(defun elfeed-view-mpv (&optional use-generic-p)
  "Youtube-feed link"
  (interactive "P")
  (let ((entries (elfeed-search-selected)))
    (cl-loop for entry in entries
     do (elfeed-untag entry 'unread)
     when (elfeed-entry-link entry)
     do (elfeed-v-mpv it))
   (mapc #'elfeed-search-update-entry entries)
   (unless (use-region-p) (forward-line))))

(define-key elfeed-search-mode-map (kbd "v") 'elfeed-view-mpv)

;; disable quit prompt
(setq confirm-kill-emacs nil)

;; disable autosave
(setq auto-save-default nil)

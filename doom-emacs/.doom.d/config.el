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
(setq doom-theme 'doom-dracula)

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

;; in case using emacs on a mac
(cond (IS-MAC
       (setq mac-command-modifier      'meta
             mac-option-modifier       'alt
             mac-right-option-modifier 'alt)))


;; styling the appearance of the org buffer to my liking.
;; borrowed many parts from https://www.grszkth.fr/blog/doom-config/
(defun davids-org-mode-visual()
  (setq visual-fill-column-width 100
        display-fill-column-indicator nil
        ;; visual-fill-column-center-text t
        display-line-numbers nil)
  (visual-fill-column-mode 1))

(after! org
  (setq ;;org-startup-folded 'overview
   org-ellipsis " ▾ "
   org-log-into-drawer 't
   org-log-done 'time
   org-log-done 'note)
  ;; ignore popup rule for source code mode in org (usually opens in a small
  ;; popup at the bottom of the screen). This will open in as a normal split
  ;; buffer (usually to the right of the original buffer)
  (set-popup-rule! "^ ?\\*Org Src[* ]" :ignore t))

(add-hook! 'org-mode-hook
            #'davids-org-mode-visual)

;; disable electric mode which creates annoying indentation in org-mode
(add-hook! org-mode (electric-indent-local-mode -1))

;; make sure that ispell language gets picked up correctly.
;; sometimes it doesn't work out of the box when the selected locale is the UK
(setq ispell-dictionary "en")

;; modeline
;; I expect most of the documents I work on to be UTF - 8, So I don’t want to
;; see that taking up space unless the encoding is something different
(defun doom-modeline-conditional-buffer-encoding ()
  (setq-local doom-modeline-buffer-encoding
              (unless (or (eq buffer-file-coding-system 'utf-8-unix)
                          (eq buffer-file-coding-system 'utf-8)))))

(add-hook 'after-change-major-mode-hook #'doom-modeline-conditional-buffer-encoding)

;; remove the asci dashboard banner
(remove-hook '+doom-dashboard-functions #'doom-dashboard-widget-banner)
;; remove the footer with link to doom's github page
(remove-hook '+doom-dashboard-functions #'doom-dashboard-widget-footer)

;; use magit-delta to show diff in magit (requires delta installed on yous system)
;; Use M-x magit-delta-mode to toggle between using delta, and normal magit
;; behavior
;; to activate automatically use this code:
;;(add-hook 'magit-mode-hook (lambda () (magit-delta-mode +1))

;; Increase Doom's default max number of delimiters of 3 to something more realistic
(setq rainbow-delimiters-max-face-count 6)

;; ESS

;; enrable rainbow delimeters in R
(after! ess
  (add-hook! 'prog-mode-hook #'rainbow-delimiters-mode)
  ;; We don’t want R evaluation to hang the editor
  (setq ess-eval-visibly 'nowait)
  ;; enable syntax highlighing in R
  (setq ess-R-font-lock-keywords
        '((ess-R-fl-keyword:keywords . t)
          (ess-R-fl-keyword:constants . t)
          (ess-R-fl-keyword:modifiers . t)
          (ess-R-fl-keyword:fun-defs . t)
          (ess-R-fl-keyword:assign-ops . t)
          (ess-R-fl-keyword:%op% . t)
          (ess-fl-keyword:fun-calls . t)
          (ess-fl-keyword:numbers . t)
          (ess-fl-keyword:operators . t)
          ;; (ess-fl-keyword:delimiters . t) ;; don't want this bc we have rainbow delimiters
          (ess-fl-keyword:= . t)
          (ess-R-fl-keyword:F&T . t)))
  ;; If I use LSP it is better to let LSP handle lintr. See example in
  ;; https://github.com/hlissner/doom-emacs/issues/2606.
  ;; (setq! ess-use-flymake nil)
  ;; (setq! lsp-ui-doc-enable nil
  ;;       lsp-ui-doc-delay 1.5)
  ;; Follow tidyverse style guide
  (setq
   ess-style 'RStudio
   ess-offset-continued 2
   ess-expression-offset 0)
  ;; move to the end of the output when evaluating code
  (setq comint-move-point-for-output t)
  ;; ESS buffers should not be cleaned up automatically
  (add-hook 'inferior-ess-mode-hook #'doom-mark-buffer-as-real-h))

;; get rid of sometimes annoying evil undo removing too much
(setq evil-want-fine-undo t
      ;; set undo linmit to 80Mb
      undo-limit 80000000)
;; take new window space from all other windows (not just current)
(setq-default window-combination-resize t
              ;; Stretch cursor to the glyph width
              x-stretch-cursor t)

;; use bash for tramp mode because using zsh will make it hang 
(eval-after-load 'tramp '(setenv "SHELL" "/bin/bash"))



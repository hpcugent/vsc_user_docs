#!/usr/bin/env runhaskell

import Text.Pandoc.JSON
import Text.Pandoc

import Debug.Trace
import System.Environment
import System.FilePath

-- | prepends the correct site directory depending on
-- the VSC_SITE env variable
filename :: Bool -> FilePath -> IO FilePath
filename True basename = do
  siteDir <- getEnv "VSC_SITE"
  return $ siteDir </> basename

filename False basename = return basename

-- | replaces Header's and Codeblock's if they have a basename variable
inline :: Block -> IO [Block]
inline h@(Header n attr text) = do
  case lookup "include" variables of
    Just v -> include v
    Nothing -> return [h]
  where
    (identifier, classes, variables) = attr
    isSpecific = "site-specific" == identifier

    -- read the file as markdown and get the blocks inside it (conveniently parsed)
    include f = do
      filename <- filename isSpecific f
      string <- readFile filename
      (Pandoc meta blocks) <- return $ readMarkdown def string
      return blocks

inline cb@(CodeBlock (identifier, classes, variables) contents) = do
    case lookup "include" variables of
      -- Here we just read the contents of the file as is, no parsing is done
      Just f     -> return . return . (CodeBlock (identifier, classes, variables)) =<< readFile' f
      Nothing    -> return [cb]
  where
    isSpecific = "site-specific" == identifier
    readFile' f = do
      name <- filename isSpecific f
      readFile name

inline x = return [x]

main = toJSONFilter inline

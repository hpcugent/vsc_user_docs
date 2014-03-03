#!/usr/bin/env runhaskell

import Text.Pandoc.JSON
import Text.Pandoc

import Debug.Trace
import System.Environment
import System.FilePath


filename True basename = do
  siteDir <- getEnv "VSC_SITE"
  return $ siteDir </> basename

filename False basename = return basename

inline :: Block -> IO [Block]
inline h@(Header n attr text) = do
  case lookup "basename" variables of
    Just v -> include v
    Nothing -> return [h]
  where
    (identifier, classes, variables) = attr
    isSpecific = "specific" == identifier

    include f = do
      filename <- filename isSpecific f
      string <- readFile filename
      (Pandoc meta blocks) <- return $ readMarkdown def string
      return blocks

inline cb@(CodeBlock (identifier, classes, variables) contents) = do
    case lookup "basename" variables of
      Just f     -> return . return . (CodeBlock (identifier, classes, variables)) =<< readFile' f
      Nothing    -> return [cb]
  where
    isSpecific = "specific" == identifier
    readFile' f = do
      name <- filename isSpecific f
      readFile name


inline x = return [x]

main = toJSONFilter inline

